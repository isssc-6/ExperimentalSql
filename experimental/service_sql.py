from experimental.connection import conn, cur
import psycopg.errors
class SqlSerivice():
    def __init__(self):
        self.conn = conn
        self.cur = cur
        self.create_table()


    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS arquivos_csv (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(200) NOT NULL,
                conteudo BYTEA NOT NULL,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.conn.commit()

    def inserir_csv(self, csv: dict):
        try:
            self.cur.execute(
                "INSERT INTO arquivos_csv (nome, conteudo) VALUES (%s, %s) RETURNING id",
                (csv['name'], csv['content'])
            )
            id = self.cur.fetchone()[0]
            self.conn.commit()
            return id
        except psycopg.Error as e:
            self.conn.rollback()
            print(f"Erro ao inserir CSVs: {e}")
            return False

    def deletar_csvs(self, ids: list[str]):
        print(ids)
        try:
            id_list = [int(id_str) for id_str in ids]
            print(id_list)
            if not id_list:
                return True
           
            self.cur.execute(
                "DELETE FROM arquivos_csv WHERE id = ANY(%s)",
                (id_list,)
            )
            self.conn.commit()
            return True
        except (psycopg.Error, ValueError) as e:
            self.conn.rollback()
            print(f"Erro ao deletar CSVs: {e}")
            return False


    def get_csvs(self, names: list[str]):
        print(names)
        self.cur.execute("SELECT id, nome, conteudo FROM arquivos_csv where id = ANY(%s)", (names,))
        rows = self.cur.fetchall()
        columns = [desc[0] for desc in self.cur.description]
        return [dict(zip(columns, row)) for row in rows]
    
    def get_all_csvs(self):
        self.cur.execute("SELECT id, nome FROM arquivos_csv")
        rows = self.cur.fetchall()
        columns = [desc[0] for desc in self.cur.description]
        return [dict(zip(columns, row)) for row in rows]