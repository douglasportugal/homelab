# 🧩 Homelab - Databases Docker

Este diretório contém configurações de bancos de dados executados em contêineres Docker, cada um com seu próprio arquivo `.env` para definir variáveis de ambiente específicas.

Cada banco possui um arquivo `.env` onde são definidas as variáveis usadas pelo respectivo `docker-compose.yml`.

---

## ⚙️ Configuração dos Arquivos `.env`

Abaixo estão os exemplos de variáveis recomendadas para cada banco.

---

## ⚙️ Exemplos de arquivos `.env` para cada banco

### 🟦 IBM DB2 (`db2/.env`)

```bash
LICENSE=accept
DB2INSTANCE=db2inst1
DB2INST1_PASSWORD=db2senhaforte
DBNAME=db2db
DB2_PORT=50000
```

### 🐬 MariaDB (`mariadb/.env`)

```bash
MARIADB_ROOT_PASSWORD=root123
MARIADB_DATABASE=homelab
MARIADB_USER=user
MARIADB_PASSWORD=mariadbsenhaforte
MARIADB_PORT=3306
```

### 🪟 Microsoft SQL Server (`mssql/.env`)

```bash
ACCEPT_EULA=Y
SA_PASSWORD=sqlserversenhaforte
MSSQL_DB=homelab
MSSQL_PORT=1433
```

### 🟠 Oracle Database (`oracle/.env`)

```bash
ORACLE_SID=ORCLCDB
ORACLE_PDB=ORCLPDB1
ORACLE_PWD=oraclesenhaforte
ORACLE_PORT=1521
ORACLE_CHARACTERSET=AL32UTF8
```

### 🐘 PostgreSQL (`postgres/.env`)

```bash
POSTGRES_DB=homelab
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgressenhaforte
POSTGRES_PORT=5432
```