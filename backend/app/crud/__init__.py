from app.crud.plot import CrudPlot
from app.crud.tree_data import CrudTreeData
from app.crud.litter_data import CrudLitterData
from app.crud.seed_data import CrudSeedData


class Crud(CrudPlot, CrudTreeData, CrudLitterData, CrudSeedData):
    pass
