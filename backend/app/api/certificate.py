from fastapi import APIRouter, Depends, Security
from app.schemas import (
    MyCertificateItem, CertificateDownloadResponse, CertificateVerification
)
from app.services import CertificateService
from app.core.di import get_certificate_service, get_user_info

certificate_router = APIRouter(prefix="/certificates", tags=["Certificates"])


@certificate_router.get("/me", response_model=list[MyCertificateItem])
async def my_certificates(
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: CertificateService = Depends(get_certificate_service),
):
    return await service.my_certificates(payload)


@certificate_router.get("/verify/{serial}", response_model=CertificateVerification,
                        description="Public: confirms a serial is authentic, no login required")
async def verify_certificate(
    serial: str,
    service: CertificateService = Depends(get_certificate_service),
):
    return await service.verify(serial)


@certificate_router.get("/{serial}/download", response_model=CertificateDownloadResponse)
async def download_certificate(
    serial: str,
    payload: dict = Security(get_user_info, scopes=["STUDENT"]),
    service: CertificateService = Depends(get_certificate_service),
):
    return await service.download(payload, serial)
