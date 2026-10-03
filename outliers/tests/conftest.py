"""Fixtures do OUTLIER → ENCAIXE. Nenhum teste usa a rede: o urlopen é trocado por um que explode."""
import copy
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dados_teste import (AQUI, GERADOR_OK, TROCAS_ORIGINAL, ANALYTICS_DENIS, VIDEOS_DENIS, c, escrever,  # noqa: E402
                         escrever_csv, montar_calendario, snapshot)


@pytest.fixture(autouse=True)
def sem_rede(monkeypatch):
    def explode(*a, **k):
        raise AssertionError("teste tentou usar a rede")
    import urllib.request
    monkeypatch.setattr(urllib.request, "urlopen", explode)


@pytest.fixture
def raiz(tmp_path):
    escrever(tmp_path / "radar" / "radar_snapshot.json", json.dumps(snapshot(), ensure_ascii=False))
    escrever_csv(tmp_path / "dados" / "videos.csv",
                 ["id", "titulo", "publicado_em_utc", "publicado_em_brt", "formato", "views"],
                 [(v, t, p, p, f, n) for v, t, p, f, n in VIDEOS_DENIS])
    escrever_csv(tmp_path / "dados" / "analytics_por_video.csv", ["video_id", "engagedViews", "subscribersGained"],
                 ANALYTICS_DENIS)
    montar_calendario(tmp_path)
    escrever(tmp_path / "pautas-canal" / "trocas.json", TROCAS_ORIGINAL)
    escrever(tmp_path / "pautas-canal" / "calendario_v3.py", GERADOR_OK)
    return tmp_path


@pytest.fixture
def cfg(raiz):
    d = copy.deepcopy(c.carregar_config(AQUI / "config.json"))
    d["caminhos"].update({
        "entrada_radar": [str(raiz / "radar" / "radar_snapshot.json")],
        "historico": str(raiz / "estado" / "historico.json"),
        "canais_radar": [str(raiz / "video_radar_channels.json")],
        "videos_denis": str(raiz / "dados" / "videos.csv"),
        "analytics_denis": str(raiz / "dados" / "analytics_por_video.csv"),
        "saida": str(raiz / "saida"), "estado": str(raiz / "estado")})
    d["calendario"].update({"csv": str(raiz / "pautas-canal" / "CALENDARIO.csv"),
                            "trocas": str(raiz / "pautas-canal" / "trocas.json"),
                            "gerador": str(raiz / "pautas-canal" / "calendario_v3.py")})
    d["trello"]["credenciais"] = [str(raiz / "nada.env")]
    d["youtube"]["credenciais"] = [str(raiz / "nada.env")]
    return d
