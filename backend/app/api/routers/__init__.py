from app.api.routers.litter_annual import router as litter_annual
from app.api.routers.litter_each import router as litter_each
from app.api.routers.plots import router as plots
from app.api.routers.seed_annual import router as seed_annual
from app.api.routers.seed_each import router as seed_each
from app.api.routers.species import router as species
from app.api.routers.tree_com_summary import router as tree_com_summary
from app.api.routers.tree_com_turnover import router as tree_com_turnover
from app.api.routers.tree_sp_summary import router as tree_sp_summary
from app.api.routers.tree_sp_turnover import router as tree_sp_turnover
from app.api.routers.upload_file import router as upload_file
from fastapi import APIRouter

router = APIRouter()

router.include_router(plots, prefix="/plots", tags=["plots"])
router.include_router(
    tree_com_summary, prefix="/tree_com_summary", tags=["tree_com_summary"]
)
router.include_router(
    tree_com_turnover, prefix="/tree_com_turnover", tags=["tree_com_turnover"]
)
router.include_router(
    tree_sp_summary, prefix="/tree_sp_summary", tags=["tree_sp_summary"]
)
router.include_router(
    tree_sp_turnover, prefix="/tree_sp_turnover", tags=["tree_sp_turnover"]
)
router.include_router(litter_each, prefix="/litter_each", tags=["litter_each"])
router.include_router(litter_annual, prefix="/litter_annual", tags=["litter_annual"])
router.include_router(seed_each, prefix="/seed_each", tags=["seed_each"])
router.include_router(seed_annual, prefix="/seed_annual", tags=["seed_annual"])
router.include_router(species, prefix="/species", tags=["species"])
router.include_router(upload_file, prefix="/upload_file", tags=["upload_file"])
