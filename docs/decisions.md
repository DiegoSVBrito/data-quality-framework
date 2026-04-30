# Decisoes Tecnicas

## ADR-001: Great Expectations over Pandera

**Status:** Aceito

**Contexto:** Framework de validacao de dados para pipeline de qualidade.

**Decisao:** Utilizar Great Expectations.

**Motivos:**
- Ecossistema mais maduro com integracao nativa a dbt, Airflow e Spark
- Expectation Suites JSON sao versionaveis e auditaveis
- Data Docs geram documentacao automatica de qualidade
- Suporte a multiplos datasources (Pandas, Spark, SQL)
- Comunidade maior e documentacao mais completa

**Trade-off:** Mais pesado que Pandera. Para validacoes simples em scripts, Pandera seria mais leve. Mas para governanca em escala, GE compensa.

## ADR-002: Data Contracts Pattern

**Status:** Aceito

**Contexto:** Formalizacao de responsabilidades sobre qualidade do dado.

**Decisao:** Implementar Data Contracts em YAML para cada fonte de dados.

**Motivos:**
- Contratos transformam qualidade de dados em processo proativo
- Schema, regras, SLAs e owner definidos em um arquivo versionavel
- Mudancas no contrato passam por code review
- Contratos sao a "interface" entre produtores e consumidores de dados

## ADR-003: Expectation Suites Versionadas

**Status:** Aceito

**Contexto:** Gerenciamento das regras de validacao ao longo do tempo.

**Decisao:** Versionar expectation suites como JSON no repositorio.

**Motivos:**
- Historico de mudancas nas regras e auditavel via git
- Code review em mudancas de qualidade
- Rollback simples em caso de regressao
- Suites sao imutaveis por versao, garantindo reprodutibilidade
