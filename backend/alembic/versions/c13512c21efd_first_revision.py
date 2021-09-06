"""first revision

Revision ID: c13512c21efd
Revises: 
Create Date: 2021-05-31 13:19:07.265275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c13512c21efd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plot_id', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('name_jp', sa.String(), nullable=True),
    sa.Column('filename', sa.String(), nullable=True),
    sa.Column('md5', sa.String(), nullable=True),
    sa.Column('dtype', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('size', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('md5')
    )
    op.create_index(op.f('ix_plots_id'), 'plots', ['id'], unique=False)
    op.create_table('litter_annual',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year', sa.Float(), nullable=True),
    sa.Column('t1', sa.String(), nullable=True),
    sa.Column('t2', sa.String(), nullable=True),
    sa.Column('inst_period', sa.Float(), nullable=True),
    sa.Column('n_collect', sa.Integer(), nullable=True),
    sa.Column('wdry_leaf', sa.Float(), nullable=True),
    sa.Column('wdry_branch', sa.Float(), nullable=True),
    sa.Column('wdry_rep', sa.Float(), nullable=True),
    sa.Column('wdry_all', sa.Float(), nullable=True),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pid'], ['plots.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_litter_annual_id'), 'litter_annual', ['id'], unique=False)
    op.create_table('litter_each',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year', sa.Float(), nullable=True),
    sa.Column('t1', sa.String(), nullable=True),
    sa.Column('t2', sa.String(), nullable=True),
    sa.Column('inst_period', sa.Float(), nullable=True),
    sa.Column('wdry_leaf', sa.Float(), nullable=True),
    sa.Column('wdry_branch', sa.Float(), nullable=True),
    sa.Column('wdry_rep', sa.Float(), nullable=True),
    sa.Column('wdry_all', sa.Float(), nullable=True),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pid'], ['plots.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_litter_each_id'), 'litter_each', ['id'], unique=False)
    op.create_table('seed_annual',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year', sa.Float(), nullable=True),
    sa.Column('t1', sa.String(), nullable=True),
    sa.Column('t2', sa.String(), nullable=True),
    sa.Column('inst_period', sa.Float(), nullable=True),
    sa.Column('species_jp', sa.String(), nullable=True),
    sa.Column('species', sa.String(), nullable=True),
    sa.Column('family', sa.String(), nullable=True),
    sa.Column('order', sa.String(), nullable=True),
    sa.Column('wdry', sa.Float(), nullable=True),
    sa.Column('number', sa.Float(), nullable=True),
    sa.Column('prop_viable', sa.Float(), nullable=True),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pid'], ['plots.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_seed_annual_id'), 'seed_annual', ['id'], unique=False)
    op.create_table('seed_each',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year', sa.Float(), nullable=True),
    sa.Column('t1', sa.String(), nullable=True),
    sa.Column('t2', sa.String(), nullable=True),
    sa.Column('inst_period', sa.Float(), nullable=True),
    sa.Column('species_jp', sa.String(), nullable=True),
    sa.Column('species', sa.String(), nullable=True),
    sa.Column('family', sa.String(), nullable=True),
    sa.Column('order', sa.String(), nullable=True),
    sa.Column('wdry', sa.Float(), nullable=True),
    sa.Column('number', sa.Float(), nullable=True),
    sa.Column('prop_viable', sa.Float(), nullable=True),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pid'], ['plots.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_seed_each_id'), 'seed_each', ['id'], unique=False)
    op.create_table('tree_com_summary',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year', sa.Float(), nullable=True),
    sa.Column('mdate', sa.String(), nullable=True),
    sa.Column('nstem', sa.Float(), nullable=True),
    sa.Column('nsp', sa.Integer(), nullable=True),
    sa.Column('ba', sa.Float(), nullable=True),
    sa.Column('b', sa.Float(), nullable=True),
    sa.Column('shannon', sa.Float(), nullable=True),
    sa.Column('richness', sa.Float(), nullable=True),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pid'], ['plots.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tree_com_turnover',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('t1', sa.Float(), nullable=True),
    sa.Column('t2', sa.Float(), nullable=True),
    sa.Column('n_m', sa.Float(), nullable=True),
    sa.Column('b_m', sa.Float(), nullable=True),
    sa.Column('r_rel', sa.Float(), nullable=True),
    sa.Column('m_rel', sa.Float(), nullable=True),
    sa.Column('p_rel', sa.Float(), nullable=True),
    sa.Column('l_rel', sa.Float(), nullable=True),
    sa.Column('r_abs', sa.Float(), nullable=True),
    sa.Column('m_abs', sa.Float(), nullable=True),
    sa.Column('p_abs', sa.Float(), nullable=True),
    sa.Column('l_abs', sa.Float(), nullable=True),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pid'], ['plots.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tree_com_turnover_id'), 'tree_com_turnover', ['id'], unique=False)
    op.create_table('tree_sp_summary',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year', sa.Float(), nullable=True),
    sa.Column('species_jp', sa.String(), nullable=True),
    sa.Column('species', sa.String(), nullable=True),
    sa.Column('family', sa.String(), nullable=True),
    sa.Column('order', sa.String(), nullable=True),
    sa.Column('n', sa.Float(), nullable=True),
    sa.Column('ba', sa.Float(), nullable=True),
    sa.Column('b', sa.Float(), nullable=True),
    sa.Column('n_prop', sa.Float(), nullable=True),
    sa.Column('ba_prop', sa.Float(), nullable=True),
    sa.Column('b_prop', sa.Float(), nullable=True),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pid'], ['plots.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tree_sp_summary_id'), 'tree_sp_summary', ['id'], unique=False)
    op.create_table('tree_sp_turnover',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('t1', sa.Float(), nullable=True),
    sa.Column('t2', sa.Float(), nullable=True),
    sa.Column('species_jp', sa.String(), nullable=True),
    sa.Column('species', sa.String(), nullable=True),
    sa.Column('family', sa.String(), nullable=True),
    sa.Column('order', sa.String(), nullable=True),
    sa.Column('n_m', sa.Float(), nullable=True),
    sa.Column('b_m', sa.Float(), nullable=True),
    sa.Column('r_rel', sa.Float(), nullable=True),
    sa.Column('m_rel', sa.Float(), nullable=True),
    sa.Column('p_rel', sa.Float(), nullable=True),
    sa.Column('l_rel', sa.Float(), nullable=True),
    sa.Column('r_abs', sa.Float(), nullable=True),
    sa.Column('m_abs', sa.Float(), nullable=True),
    sa.Column('p_abs', sa.Float(), nullable=True),
    sa.Column('l_abs', sa.Float(), nullable=True),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pid'], ['plots.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tree_sp_turnover_id'), 'tree_sp_turnover', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tree_sp_turnover_id'), table_name='tree_sp_turnover')
    op.drop_table('tree_sp_turnover')
    op.drop_index(op.f('ix_tree_sp_summary_id'), table_name='tree_sp_summary')
    op.drop_table('tree_sp_summary')
    op.drop_index(op.f('ix_tree_com_turnover_id'), table_name='tree_com_turnover')
    op.drop_table('tree_com_turnover')
    op.drop_table('tree_com_summary')
    op.drop_index(op.f('ix_seed_each_id'), table_name='seed_each')
    op.drop_table('seed_each')
    op.drop_index(op.f('ix_seed_annual_id'), table_name='seed_annual')
    op.drop_table('seed_annual')
    op.drop_index(op.f('ix_litter_each_id'), table_name='litter_each')
    op.drop_table('litter_each')
    op.drop_index(op.f('ix_litter_annual_id'), table_name='litter_annual')
    op.drop_table('litter_annual')
    op.drop_index(op.f('ix_plots_id'), table_name='plots')
    op.drop_table('plots')
    # ### end Alembic commands ###
