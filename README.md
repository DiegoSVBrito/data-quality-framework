# Data Quality Framework

Framework de qualidade e governanca de dados com Great Expectations: validacao de schemas, testes de integridade, data contracts e relatorios automatizados.

## Arquitetura

```
+------------------+     +------------------+     +------------------+
|   Data Source    |     |   Great          |     |   Report +       |
|   (BigQuery /    |---->|   Expectations   |     |   Alert          |
|    CSV / API)    |     |   Validator      |     |                  |
+------------------+     +--------+---------+     +--------+---------+
                                  |                        |
                         +--------v---------+              |
                         |  Expectation     |              |
                         |  Suites          |     +--------v---------+
                         |  (transaction,   |     |   Data Contract  |
                         |   customer)      |     |   (YAML schema)  |
                         +------------------+     +------------------+
                                  |
                    +-------------+-------------+
                    |                           |
           +--------v---------+       +---------v--------+
           |  PASS            |       |  FAIL            |
           |  Data -> DW      |       |  DLQ + Notify    |
           |  (trust in data) |       |  (Slack/Email)   |
           +------------------+       +------------------+
```

## Data Contracts

Cada fonte de dados possui um contrato definido em YAML:

- **Schema**: Tipos, campos obrigatorios, restricoes
- **Quality Rules**: Faixas de valor, unicidade, integridade referencial
- **SLAs**: Frequencia de validacao, tempo maximo de resolucao
- **Owner**: Responsavel pela qualidade daquela fonte

## Como Usar

```bash
# Instalar dependencias
pip install -r requirements.txt

# Executar validacao completa
python scripts/run_validation.py --suite transaction_suite

# Gerar expectation suite a partir de profiling
python scripts/generate_expectations.py --data ./data/sample.csv

# Validar contrato
python scripts/run_validation.py --contract contracts/transaction_contract.yaml
```

## Quality Rules Implementadas

| Regra | Tipo | Descricao |
|-------|------|-----------|
| `expect_column_values_to_not_be_null` | Integridade | Campos obrigatorios sem null |
| `expect_column_values_to_be_unique` | Unicidade | IDs sem duplicata |
| `expect_column_values_to_be_between` | Faixa | Valores dentro do intervalo esperado |
| `expect_column_values_to_match_regex` | Formato | Email, CPF com formato valido |
| `expect_table_row_count_to_be_between` | Volume | Quantidade de registros dentro do esperado |

## Decisoes Tecnicas

**Por que Great Expectations e nao Pandera?** GE tem ecossistema mais maduro: expectation suites reutilizaveis, data docs automaticas, integracao com dbt/Airflow. Pandera e mais leve mas limitado para governanca em escala. GE permite versionar expectations junto com o codigo.

**Por que Data Contracts?** Contratos formalizam a responsabilidade sobre a qualidade do dado. Em vez de testes ad-hoc, cada fonte tem um contrato que define: o que e esperado, quem e responsavel, e o que acontece quando falha. Isso transforma qualidade de dados de atividade reativa em processo proativo.

**Por que Expectation Suites versionadas?** Suites sao JSON versionados no git. Mudancas na qualidade do dado passam por code review, igual mudancas no codigo. Historico de mudancas nas regras e auditavel.

## Estrutura

```
data-quality-framework/
  expectations/              # Great Expectations suites (JSON)
    transaction_suite.json
    customer_suite.json
  contracts/                 # Data Contracts (YAML)
    transaction_contract.yaml
    customer_contract.yaml
  scripts/
    run_validation.py        # Executar validacoes
    generate_expectations.py # Auto-gerar suites
  src/
    validators/              # Validadores customizados
      base_validator.py
      transaction_validator.py
      customer_validator.py
    notifiers/               # Alertas
      slack_notifier.py
      email_notifier.py
    reports/
      quality_report.py      # Relatorios HTML
  tests/
    test_validators.py
    test_contracts.py
  .github/
    workflows/
      quality-check.yml      # CI: validacao em sample data
  docs/
    decisions.md             # Architecture Decision Records
```

---

**Autor:** Diego Brito
