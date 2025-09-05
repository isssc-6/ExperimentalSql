from fastapi import APIRouter, UploadFile, File, Form, Body
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List
from io import BytesIO
import requests

from experimental.service_sql import SqlSerivice


router_experimental = APIRouter()
@router_experimental.post(
    "/sql/cadastar_csvs/",
    tags=["sql"],
)
async def inserir_csvs(
    docs: List[UploadFile] = File(description="Arquivo com os dados para a resposta"),
):    
    try:
        files = []
        ids = []
        sql_service = SqlSerivice()
        for doc in docs:
            name = doc.filename
            content = await doc.read()
            csv = {
                "name": name,
                "content": content
            }
        
            id_csv = sql_service.inserir_csv(csv)

            file = ("docs", (doc.filename, BytesIO(content), doc.content_type))
            files.append(file)

            ids.append(id_csv)

        data = {
            "ids": ids
        }
        r = requests.post(
            "http://backend:8000/vectorDb/cadastar/",
            files=files,
            data=data
        )
        

        
        if r:
            return JSONResponse(
                status_code=200,
                content={"detail": "CSVs cadastrados com sucesso."},
            )
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Erro ao cadastrar CSVs: {e}"},
        )

@router_experimental.get(
    "/sql/get_csvs/{id}",
    tags=["sql"],
)
async def get_csvs(id: int):
    sql_service = SqlSerivice()
    ids = [str(id)]
    response = sql_service.get_csvs(ids)

    return StreamingResponse(
        BytesIO(response[0]["conteudo"]),  
        media_type="text/csv",
        headers={
            "file-name":response[0]["nome"]
        }
    )

@router_experimental.post(
    "/sql/deletar_csvs/",
    tags=["sql"],
)
async def deletar_csvs(
    ids: List[str] = Body(description="IDs dos CSVs a serem deletados"),
):    
    
    sql_service = SqlSerivice()
    response = sql_service.deletar_csvs(ids)
    
    r = requests.post(
        "http://localhost:8000/vectorDb/deletar/",
        json=ids
    )
    print(r.json())
    
    if response:
        return JSONResponse(
            status_code=200,
            content={"detail": "CSVs deletados com sucesso."},
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro ao deletar CSVs."},
    )

@router_experimental.get(
    "/sql/get_all_csvs/",
    tags=["sql"],
)
async def get_all_csvs():
    sql_service = SqlSerivice()
    response =  sql_service.get_all_csvs()
    return response