from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, nullable=False)
    platform = Column(String, nullable=False)  # e.g. meta, google, tiktok
    objective = Column(String)
    brand_name = Column(String)
    ad_account_id = Column(String)
    created_at = Column(TIMESTAMP, nullable=False)

    snapshots = relationship("PerformanceSnapshot", back_populates="campaign")
    recommendations = relationship("Recommendation", back_populates="campaign")

class PerformanceSnapshot(Base):
    __tablename__ = "performance_snapshots"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)
    impressions = Column(Integer)
    clicks = Column(Integer)
    spend = Column(Float)
    purchases = Column(Integer)
    revenue = Column(Float)
    cpc = Column(Float)
    cpa = Column(Float)
    roas = Column(Float)

    campaign = relationship("Campaign", back_populates="snapshots")
    recommendations = relationship("Recommendation", back_populates="snapshot")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    snapshot_id = Column(Integer, ForeignKey("performance_snapshots.id"))
    generated_at = Column(TIMESTAMP)
    strategy_type = Column(String)
    reasoning = Column(String)
    action = Column(String)

    campaign = relationship("Campaign", back_populates="recommendations")
    snapshot = relationship("PerformanceSnapshot", back_populates="recommendations")
