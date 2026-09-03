"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-09-03
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

UUID = postgresql.UUID(as_uuid=True)


def upgrade() -> None:
    op.create_table(
        "honey_companies",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("domain", sa.String(255)),
        sa.Column("region", sa.String(100)),
        sa.Column("company_type", sa.String(100)),
        sa.Column("description", sa.Text()),
        sa.Column("export_tier", sa.String(50)),
        sa.Column("marketplace_status", sa.String(200)),
        sa.Column("estimated_employees", sa.String(50)),
        sa.Column("india_fit_score", sa.Float()),
        sa.Column("product_market_fit", sa.Float()),
        sa.Column("premium_positioning", sa.Float()),
        sa.Column("export_readiness", sa.Float()),
        sa.Column("production_scale", sa.Float()),
        sa.Column("manuka_exposure", sa.Float()),
        sa.Column("operational_readiness", sa.Float()),
    )

    op.create_table(
        "indian_companies",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("domain", sa.String(255)),
        sa.Column("city", sa.String(100)),
        sa.Column("state", sa.String(100)),
        sa.Column("description", sa.Text()),
        sa.Column("company_type", sa.String(50), nullable=False),
        sa.Column("estimated_revenue", sa.String(50)),
        sa.Column("estimated_employees", sa.String(50)),
        sa.Column("honey_category_active", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("existing_nz_imports", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("buyer_score", sa.Float()),
        sa.Column("relevance_score", sa.Float()),
        sa.Column("product_fit", sa.Float()),
        sa.Column("purchasing_capability", sa.Float()),
        sa.Column("distribution_footprint", sa.Float()),
        sa.Column("premium_compatibility", sa.Float()),
        sa.Column("evidence_quality", sa.Float()),
    )

    op.create_table(
        "agent_runs",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime()),
        sa.Column("agent_type", sa.String(100), nullable=False),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("input_summary", sa.Text()),
        sa.Column("output_summary", sa.Text()),
        sa.Column("error_message", sa.Text()),
        sa.Column("tokens_used", sa.Integer()),
        sa.Column("api_calls_made", sa.Integer()),
        sa.Column("estimated_cost_usd", sa.Float()),
    )

    op.create_table(
        "markets",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("gdp", sa.String(50)),
        sa.Column("population", sa.String(50)),
        sa.Column("honey_import_volume", sa.String(100)),
        sa.Column("honey_per_capita", sa.String(50)),
    )

    op.create_table(
        "market_segments",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("segment_type", sa.String(100), nullable=False),
        sa.Column("estimated_size", sa.String(100)),
        sa.Column("growth_rate", sa.String(50)),
        sa.Column("cities", sa.Text()),
        sa.Column("relevance_to_nz_honey", sa.Float()),
        sa.Column("market_id", UUID, sa.ForeignKey("markets.id"), nullable=False),
    )

    op.create_table(
        "data_sources",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("source_type", sa.String(50), nullable=False),
        sa.Column("url", sa.String(1000)),
        sa.Column("description", sa.Text()),
        sa.Column("reliability", sa.String(50)),
        sa.Column("last_accessed", sa.DateTime()),
    )

    op.create_table(
        "regulations",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("authority", sa.String(255)),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("requirements", sa.Text()),
        sa.Column("relevant_for", sa.String(100)),
        sa.Column("product_category", sa.String(100)),
    )

    op.create_table(
        "certifications",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("issuing_body", sa.String(255)),
        sa.Column("country", sa.String(100)),
        sa.Column("description", sa.Text()),
        sa.Column("required_for_india", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("relevant_for", sa.String(100)),
    )

    op.create_table(
        "tariffs",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("hs_code", sa.String(20), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("origin_country", sa.String(100), nullable=False),
        sa.Column("destination_country", sa.String(100), nullable=False),
        sa.Column("duty_rate", sa.String(50)),
        sa.Column("additional_duties", sa.String(255)),
        sa.Column("gst_rate", sa.String(50)),
        sa.Column("effective_date", sa.String(50)),
        sa.Column("notes", sa.Text()),
    )

    op.create_table(
        "competitors",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("country", sa.String(100)),
        sa.Column("company_type", sa.String(100)),
        sa.Column("description", sa.Text()),
        sa.Column("estimated_volume", sa.String(100)),
        sa.Column("positioning", sa.String(255)),
        sa.Column("distribution", sa.Text()),
    )

    op.create_table(
        "contacts",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("title", sa.String(255)),
        sa.Column("email", sa.String(255)),
        sa.Column("phone", sa.String(50)),
        sa.Column("linkedin_url", sa.String(500)),
        sa.Column("source", sa.String(100)),
        sa.Column("email_confidence", sa.Float()),
        sa.Column("honey_company_id", UUID, sa.ForeignKey("honey_companies.id")),
        sa.Column("indian_company_id", UUID, sa.ForeignKey("indian_companies.id")),
    )

    op.create_table(
        "honey_products",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("honey_type", sa.String(100)),
        sa.Column("umf_mgo", sa.String(50)),
        sa.Column("grade", sa.String(50)),
        sa.Column("volume_capacity", sa.String(100)),
        sa.Column("description", sa.Text()),
        sa.Column("estimated_price_nzd", sa.Float()),
        sa.Column("estimated_price_per_kg", sa.Float()),
        sa.Column("organic", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("manuka_certified", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("honey_company_id", UUID, sa.ForeignKey("honey_companies.id"), nullable=False),
    )

    op.create_table(
        "trade_flows",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("hs_code", sa.String(20)),
        sa.Column("product_description", sa.String(255)),
        sa.Column("volume_tonnes", sa.Float()),
        sa.Column("value_usd", sa.Float()),
        sa.Column("year", sa.Integer()),
        sa.Column("origin_country", sa.String(100), nullable=False),
        sa.Column("destination_country", sa.String(100), nullable=False),
        sa.Column("trade_route", sa.String(255)),
        sa.Column("honey_company_id", UUID, sa.ForeignKey("honey_companies.id")),
        sa.Column("indian_company_id", UUID, sa.ForeignKey("indian_companies.id")),
    )

    op.create_table(
        "evidence",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("claim", sa.Text(), nullable=False),
        sa.Column("claim_type", sa.String(100)),
        sa.Column("source_url", sa.String(1000)),
        sa.Column("source_title", sa.String(500)),
        sa.Column("source_type", sa.String(50)),
        sa.Column("retrieved_at", sa.DateTime(), nullable=False),
        sa.Column("published_at", sa.DateTime()),
        sa.Column("extracted_text", sa.Text()),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("data_source_id", UUID, sa.ForeignKey("data_sources.id")),
        sa.Column("honey_company_id", UUID, sa.ForeignKey("honey_companies.id")),
        sa.Column("indian_company_id", UUID, sa.ForeignKey("indian_companies.id")),
    )

    op.create_table(
        "opportunities",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("stage", sa.String(50), nullable=False),
        sa.Column("score", sa.Float()),
        sa.Column("buying_hypothesis", sa.Text()),
        sa.Column("reason_for_fit", sa.Text()),
        sa.Column("honey_company_id", UUID, sa.ForeignKey("honey_companies.id"), nullable=False),
        sa.Column("indian_company_id", UUID, sa.ForeignKey("indian_companies.id"), nullable=False),
    )

    op.create_table(
        "recommendations",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("recommendation_type", sa.String(100), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("priority", sa.String(20), nullable=False),
        sa.Column("opportunity_id", UUID, sa.ForeignKey("opportunities.id"), nullable=False),
    )

    op.create_table(
        "research_reports",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("report_type", sa.String(100), nullable=False),
        sa.Column("content", sa.Text()),
        sa.Column("summary", sa.Text()),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("honey_company_id", UUID, sa.ForeignKey("honey_companies.id")),
        sa.Column("agent_run_id", UUID, sa.ForeignKey("agent_runs.id")),
    )

    op.create_table(
        "outreach",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("channel", sa.String(50), nullable=False),
        sa.Column("subject", sa.String(500)),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("personalization_evidence", sa.Text()),
        sa.Column("opportunity_id", UUID, sa.ForeignKey("opportunities.id"), nullable=False),
        sa.Column("contact_id", UUID, sa.ForeignKey("contacts.id")),
    )

    op.create_table(
        "conversations",
        sa.Column("id", UUID, primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("subject", sa.String(500)),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("notes", sa.Text()),
        sa.Column("next_action", sa.Text()),
        sa.Column("opportunity_id", UUID, sa.ForeignKey("opportunities.id")),
    )

    op.create_index("ix_evidence_honey_company_id", "evidence", ["honey_company_id"])
    op.create_index("ix_evidence_indian_company_id", "evidence", ["indian_company_id"])
    op.create_index("ix_contacts_honey_company_id", "contacts", ["honey_company_id"])
    op.create_index("ix_contacts_indian_company_id", "contacts", ["indian_company_id"])


def downgrade() -> None:
    op.drop_table("conversations")
    op.drop_table("outreach")
    op.drop_table("research_reports")
    op.drop_table("recommendations")
    op.drop_table("opportunities")
    op.drop_table("evidence")
    op.drop_table("trade_flows")
    op.drop_table("honey_products")
    op.drop_table("contacts")
    op.drop_table("competitors")
    op.drop_table("tariffs")
    op.drop_table("certifications")
    op.drop_table("regulations")
    op.drop_table("data_sources")
    op.drop_table("market_segments")
    op.drop_table("markets")
    op.drop_table("agent_runs")
    op.drop_table("indian_companies")
    op.drop_table("honey_companies")
