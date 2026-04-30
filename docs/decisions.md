# Technical Decisions

## ADR-001: Great Expectations over Pandera

**Status:** Accepted

**Context:** Data validation framework for quality pipeline.

**Decision:** Use Great Expectations.

**Rationale:**
- More mature ecosystem with native dbt, Airflow, Spark integration
- JSON Expectation Suites are versionable and auditable
- Data Docs auto-generate quality documentation
- Multiple datasource support (Pandas, Spark, SQL)
- Larger community and more complete documentation

**Trade-off:** Heavier than Pandera. For simple validations in scripts, Pandera would be lighter. But for governance at scale, GE is worth it.

## ADR-002: Data Contracts Pattern

**Status:** Accepted

**Context:** Formalizing responsibilities for data quality.

**Decision:** Implement Data Contracts in YAML for each data source.

**Rationale:**
- Contracts make data quality a proactive process
- Schema, rules, SLAs, and owner defined in a versioned file
- Contract changes go through code review
- Contracts serve as the interface between data producers and consumers

## ADR-003: Versioned Expectation Suites

**Status:** Accepted

**Context:** Managing validation rules over time.

**Decision:** Version expectation suites as JSON in the repository.

**Rationale:**
- Change history is auditable via git
- Code review on quality changes
- Simple rollback on regressions
- Suites are immutable per version, ensuring reproducibility
