from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
from rag.retriever import retrieve_knowledge as rag_retrieve_knowledge


# ============================================================
# ECO MIND - AI BIODIVERSITY INTELLIGENCE SYSTEM
# ============================================================

app = FastAPI(
    title="EcoMind AI Biodiversity Intelligence System",
    version="2.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "frontend"
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

KNOWLEDGE_FILE = os.path.join(
    DATA_DIR,
    "biodiversity_knowledge.json"
)


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

def load_knowledge():

    try:
        with open(
            KNOWLEDGE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as error:

        print("Knowledge base loading error:", error)

        return []


KNOWLEDGE_BASE = load_knowledge()


# ============================================================
# FRONTEND ROUTES
# ============================================================

@app.get("/")
def home():

    return FileResponse(
        os.path.join(
            FRONTEND_DIR,
            "index.html"
        )
    )


@app.get("/analysis.html")
def analysis_page():

    return FileResponse(
        os.path.join(
            FRONTEND_DIR,
            "analysis.html"
        )
    )


@app.get("/login.html")
def chat_page():

    return FileResponse(
        os.path.join(
            FRONTEND_DIR,
            "login.html"
        )
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
def health():

    return {
        "status": "online",
        "system": "EcoMind",
        "knowledge_base": len(KNOWLEDGE_BASE),
        "message": "AI Biodiversity Intelligence System is running"
    }


# ============================================================
# ENVIRONMENTAL ANALYSIS MODEL
# ============================================================

class EnvironmentalData(BaseModel):

    species: str
    location: str
    ph: float
    organic_carbon: float
    soil_moisture: float
    temperature: float
    rainfall: float
    land_use: str


# ============================================================
# CHAT MODEL
# ============================================================

class ChatRequest(BaseModel):

    message: str


# ============================================================
# KNOWLEDGE RETRIEVAL
# ============================================================

def retrieve_knowledge(message):

    message_lower = message.lower()

    results = []

    for item in KNOWLEDGE_BASE:

        score = 0

        keywords = item.get(
            "keywords",
            []
        )

        topic = item.get(
            "topic",
            ""
        )

        text = (
            str(keywords)
            + " "
            + str(topic)
            + " "
            + str(item.get("condition", ""))
        ).lower()

        for keyword in keywords:

            if str(keyword).lower() in message_lower:
                score += 2

        if topic.lower() in message_lower:
            score += 2

        if score > 0:

            results.append(
                (
                    score,
                    item
                )
            )

    results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        item
        for score, item in results[:3]
    ]


# ============================================================
# CHAT INTELLIGENCE
# ============================================================

def generate_chat_response(message):

    text = message.lower()

    retrieved = rag_retrieve_knowledge(message)


    # --------------------------------------------------------
    # LOW RAINFALL + SOIL MOISTURE
    # --------------------------------------------------------

    if (
        ("rainfall" in text or "rain" in text)
        and
        ("moisture" in text or "dry" in text or "water" in text)
    ):

        recommendation = (
            "Increase vegetation cover and use water-conserving "
            "land management practices. Suitable cover crops, "
            "organic matter management and maintaining ground cover "
            "can help reduce moisture loss."
        )

        why = (
            "Vegetation cover can protect the soil surface and help "
            "retain moisture. Better soil conditions can also support "
            "soil organisms and plant growth."
        )

        metrics = [
            "Soil moisture",
            "Water availability",
            "Soil biological activity",
            "Habitat quality"
        ]


    # --------------------------------------------------------
    # LOW ORGANIC CARBON
    # --------------------------------------------------------

    elif (
        "organic carbon" in text
        or
        "soil carbon" in text
        or
        "low carbon" in text
    ):

        recommendation = (
            "Increase organic matter inputs using suitable compost, "
            "crop residues, cover crops or other locally appropriate "
            "organic amendments."
        )

        why = (
            "Soil organic matter influences soil structure, water "
            "infiltration, moisture holding capacity and biological "
            "activity. Improving organic matter can therefore connect "
            "soil health with biodiversity."
        )

        metrics = [
            "Soil organic carbon",
            "Soil health",
            "Soil biological activity",
            "Water retention"
        ]


    # --------------------------------------------------------
    # MONOCULTURE
    # --------------------------------------------------------

    elif (
        "monoculture" in text
        or
        "single crop" in text
        or
        "one crop" in text
    ):

        recommendation = (
            "Introduce suitable crop diversity through intercropping, "
            "native flowering strips, hedgerows or other habitat "
            "features appropriate to the site."
        )

        why = (
            "Increasing vegetation and habitat diversity can provide "
            "more ecological niches and resources for pollinators "
            "and other organisms."
        )

        metrics = [
            "Habitat diversity",
            "Biodiversity",
            "Pollinator resources",
            "Ecological connectivity"
        ]


    # --------------------------------------------------------
    # POLLINATORS
    # --------------------------------------------------------

    elif (
        "pollinator" in text
        or
        "bee" in text
        or
        "butterfly" in text
    ):

        recommendation = (
            "Maintain or establish native flowering vegetation and "
            "connected habitat areas that provide food and shelter "
            "through different parts of the growing season."
        )

        why = (
            "A greater variety of flowering plants and habitat "
            "structures can provide resources for pollinators and "
            "increase habitat diversity."
        )

        metrics = [
            "Pollinator resources",
            "Habitat diversity",
            "Species richness",
            "Ecological connectivity"
        ]


    # --------------------------------------------------------
    # HIGH TEMPERATURE
    # --------------------------------------------------------

    elif (
        "temperature" in text
        or
        "heat" in text
        or
        "hot" in text
    ):

        recommendation = (
            "Increase native vegetation cover and maintain shaded "
            "habitat areas where appropriate to provide cooler "
            "microhabitats."
        )

        why = (
            "Temperature affects species physiology, distribution "
            "and ecological conditions. Vegetation can also create "
            "microclimatic variation within a landscape."
        )

        metrics = [
            "Temperature stress",
            "Habitat quality",
            "Species survival",
            "Vegetation health"
        ]


    # --------------------------------------------------------
    # WATER / BIODIVERSITY
    # --------------------------------------------------------

    elif (
        "water" in text
        or
        "drought" in text
        or
        "dry" in text
    ):

        recommendation = (
            "Protect water availability by maintaining vegetation "
            "cover, reducing unnecessary soil exposure and protecting "
            "important wet areas or water sources."
        )

        why = (
            "Water availability influences vegetation growth and "
            "freshwater and terrestrial biodiversity. Changes in "
            "precipitation and drought conditions can affect species "
            "survival and habitat quality."
        )

        metrics = [
            "Water availability",
            "Soil moisture",
            "Habitat quality",
            "Biodiversity"
        ]


    # --------------------------------------------------------
    # GENERAL BIODIVERSITY
    # --------------------------------------------------------

    elif (
        "biodiversity" in text
        or
        "species" in text
        or
        "habitat" in text
    ):

        recommendation = (
            "Increase habitat diversity by maintaining native "
            "vegetation, ecological buffer areas and a mixture of "
            "habitat structures suited to the local ecosystem."
        )

        why = (
            "Habitat diversity can provide different food, shelter "
            "and breeding opportunities for organisms and can support "
            "greater species diversity."
        )

        metrics = [
            "Species richness",
            "Habitat diversity",
            "Ecological connectivity",
            "Biodiversity"
        ]


    # --------------------------------------------------------
    # GENERAL ENVIRONMENTAL QUESTION
    # --------------------------------------------------------

    else:

        recommendation = (
            "Consider the interaction between soil health, water "
            "availability, climate conditions and land-use patterns "
            "before selecting an intervention."
        )

        why = (
            "Environmental conditions are interconnected. Changes "
            "in soil, water, climate or land use can influence habitat "
            "quality and biodiversity."
        )

        metrics = [
            "Soil health",
            "Water availability",
            "Climate conditions",
            "Habitat diversity",
            "Biodiversity"
        ]


    # ========================================================
    # SCIENTIFIC EVIDENCE
    # ========================================================

    evidence = []

    for item in retrieved:

        evidence.append({
            "topic": item.get(
                "topic",
                "Environmental knowledge"
            ),
            "evidence": item.get(
                "evidence",
                ""
            ),
            "source": item.get(
                "source",
                "Scientific environmental literature"
            ),
            "source_url": item.get(
                "source_url",
                ""
            )
        })


    # If no exact keyword match
    if not evidence:

        evidence.append({
            "topic": "Environmental biodiversity",
            "evidence": (
                "Scientific assessments show that soil, water, "
                "climate and habitat conditions interact to influence "
                "ecosystem functioning and biodiversity."
            ),
            "source": "FAO and IPCC environmental assessments",
            "source_url": ""
        })


    return {
        "system": "EcoMind",

        "message": message,

        "answer": {
            "recommendation": recommendation,
            "why": why,
            "affected_metrics": metrics,
            "time_horizon": "Medium term: approximately 1–3 years",
            "confidence": "Preliminary evidence-grounded assessment"
        },

        "evidence": evidence,

        "retrieved_documents": len(retrieved)
    }


# ============================================================
# CHAT API
# ============================================================

@app.post("/api/chat")
def chat(request: ChatRequest):

    return generate_chat_response(
        request.message
    )


# ============================================================
# ENVIRONMENTAL ANALYSIS
# ============================================================

@app.post("/api/analyze")
def analyze_environment(
    data: EnvironmentalData
):

    # --------------------------------------------------------
    # SOIL PH
    # --------------------------------------------------------

    if data.ph < 5.5:

        soil_status = (
            "Acidic soil conditions detected."
        )

    elif data.ph > 8.0:

        soil_status = (
            "Alkaline soil conditions detected."
        )

    else:

        soil_status = (
            "Soil pH is within a generally suitable range."
        )


    # --------------------------------------------------------
    # ORGANIC CARBON
    # --------------------------------------------------------

    if data.organic_carbon < 0.8:

        carbon_status = (
            "Low soil organic carbon may limit soil biological activity."
        )

    else:

        carbon_status = (
            "Soil organic carbon provides a reasonable baseline."
        )


    # --------------------------------------------------------
    # WATER
    # --------------------------------------------------------

    if (
        data.soil_moisture < 30
        or
        data.rainfall < 500
    ):

        water_status = (
            "Water availability may be a limiting ecological factor."
        )

    else:

        water_status = (
            "Water availability provides a moderate ecological baseline."
        )


    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    if data.temperature > 35:

        temperature_status = (
            "Higher temperatures may increase environmental stress "
            "for some species."
        )

    elif data.temperature < 10:

        temperature_status = (
            "Lower temperatures may influence species activity "
            "and vegetation growth."
        )

    else:

        temperature_status = (
            "Temperature conditions are within a moderate range."
        )


    # --------------------------------------------------------
    # LAND USE
    # --------------------------------------------------------

    if data.land_use == "Monoculture":

        land_status = (
            "Monoculture can reduce habitat diversity and available "
            "ecological niches."
        )

    elif data.land_use == "Urban area":

        land_status = (
            "Urban land use can increase habitat fragmentation "
            "and ecological pressure."
        )

    elif data.land_use == "Forest":

        land_status = (
            "Forest land can provide structurally diverse habitat "
            "for multiple species."
        )

    elif data.land_use == "Wetland":

        land_status = (
            "Wetland habitat can support diverse aquatic and "
            "terrestrial organisms."
        )

    elif data.land_use == "Grassland":

        land_status = (
            "Grassland can provide open habitat and resources "
            "for a range of species."
        )

    else:

        land_status = (
            "Mixed land use can provide opportunities for greater "
            "habitat diversity."
        )


    # --------------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------------

    if data.land_use == "Monoculture":

        recommendation = (
            "Introduce native flowering strips, hedgerows or suitable "
            "intercrops around the cultivated area to increase habitat diversity."
        )

        impact = (
            "Improved habitat diversity, pollinator resources "
            "and ecological connectivity."
        )

        affected_metrics = [
            "Habitat diversity",
            "Biodiversity",
            "Pollinator resources"
        ]


    elif data.organic_carbon < 0.8:

        recommendation = (
            "Increase organic matter inputs through practices such as "
            "compost, crop residues or suitable cover crops."
        )

        impact = (
            "Potential improvement in soil organic carbon "
            "and soil biological activity."
        )

        affected_metrics = [
            "Soil organic carbon",
            "Soil health",
            "Soil biological activity"
        ]


    elif data.soil_moisture < 30:

        recommendation = (
            "Increase vegetation cover and use water-conserving "
            "land management to improve moisture retention."
        )

        impact = (
            "Potential improvement in soil moisture availability "
            "and vegetation support."
        )

        affected_metrics = [
            "Soil moisture",
            "Water availability",
            "Vegetation health"
        ]


    elif data.temperature > 35:

        recommendation = (
            "Increase native vegetation cover and maintain shaded "
            "habitat areas to provide microclimatic refuges."
        )

        impact = (
            "Potential reduction of heat exposure "
            "and improved habitat conditions."
        )

        affected_metrics = [
            "Temperature stress",
            "Habitat quality",
            "Species survival"
        ]


    else:

        recommendation = (
            "Maintain habitat diversity using native vegetation, "
            "mixed land use and ecological buffer areas."
        )

        impact = (
            "Supports habitat availability, species resources "
            "and ecological resilience."
        )

        affected_metrics = [
            "Biodiversity",
            "Habitat diversity",
            "Ecological resilience"
        ]


    # ========================================================
    # RETURN ANALYSIS
    # ========================================================

    return {

        "system": "EcoMind",

        "species": data.species,

        "location": data.location,

        "input": {
            "species": data.species,
            "location": data.location,
            "soil_ph": data.ph,
            "organic_carbon": data.organic_carbon,
            "soil_moisture": data.soil_moisture,
            "temperature": data.temperature,
            "rainfall": data.rainfall,
            "land_use": data.land_use
        },

        "assessment": {

            "soil": soil_status,

            "organic_carbon": carbon_status,

            "water": water_status,

            "temperature": temperature_status,

            "land_use": land_status
        },

        "recommendation": recommendation,

        "impact": impact,

        "affected_metrics": affected_metrics,

        "metrics": [

            "Soil health",
            "Soil organic carbon",
            "Soil moisture",
            "Water availability",
            "Temperature",
            "Habitat diversity",
            "Biodiversity"

        ],

        "time_horizon": (
            "Medium term: approximately 1–3 years"
        ),

        "confidence": (
            "Preliminary assessment"
        )

    }