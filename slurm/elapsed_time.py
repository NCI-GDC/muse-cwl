import postgres

class Time(postgres.ToolTypeMixin, postgres.Base):

    __tablename__ = 'muse_cwl_metrics'
