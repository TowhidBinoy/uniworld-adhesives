import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniworld.settings')
django.setup()

from product.models import Category, Industry, Product, ProductImage, Contact

print("Clearing old records...")
ProductImage.objects.all().delete()
Product.objects.all().delete()
Category.objects.all().delete()
Industry.objects.all().delete()
Contact.objects.all().delete()

# 1. Create Categories (Lowercase slugs per SEO Audit)
cat_footwear = Category.objects.create(
    name="Footwear",
    slug="footwear",
    meta_title="Footwear Adhesives & Primers for Shoe Making | Uniworld",
    meta_description="Shoe-making adhesives for EVA, PU, PVC and leather: graft CR, synthetic rubber and PU adhesives, plus primers and sole cleaner. Bulk supply across Bangladesh.",
    h1_title="Footwear Adhesives, Primers & Cleaners",
    content="<p>Uniworld manufactures complete sole-to-upper bonding systems engineered for Bangladesh's export and domestic footwear factories. From halogenated EVA and PU/PVC surface primers to heat-activated Polyurethane (PU) and Grafted Chloroprene (Graft CR) adhesives, every grade is tested for flex-crack resistance and tropical heat stability.</p>",
    buying_guide="<p><strong>How to choose:</strong> Use <strong>PU Adhesive</strong> (Standard or Premium) for PVC, PU, and synthetic leather uppers. For molded EVA or Phylon soles, treat with <strong>EVA Primer</strong> first and bond using <strong>Graft CR Adhesive</strong>.</p>",
    faqs=[
        {"question": "Which adhesive works best for EVA shoe soles?", "answer": "Clean the sole with Synthetic Cleaner, apply one thin coat of Uniworld EVA Primer, let dry for 3–5 minutes, and bond with Graft CR Adhesive or Premium PU Adhesive."},
        {"question": "What heat activation temperature is recommended for Uniworld PU adhesives?", "answer": "Heat-activate dried adhesive films at 60°C–70°C for 10–15 seconds before pressing in a sole-attaching press."}
    ]
)

cat_furniture = Category.objects.create(
    name="Furniture",
    slug="furniture",
    meta_title="Furniture & Foam Adhesives: SBS Spray & PU | Uniworld",
    meta_description="SBS sprayable and polyurethane adhesives for furniture, foam and woodworking. Fast tack and a strong, flexible hold for manual or semi-auto production lines.",
    h1_title="Furniture & Woodworking Adhesives",
    content="<p>Engineered for mattress manufacturers, sofa upholstery lines, and commercial woodworking workshops across Bangladesh. Uniworld's low-viscosity SBS sprayable grades atomize cleanly through standard spray guns without cobwebbing, while our heavy-bodied Synthetic Rubber contact adhesives provide long open tack time for HPL laminates and veneers.</p>",
    buying_guide="<p><strong>How to choose:</strong> Use <strong>SBS Sprayable Adhesive</strong> or <strong>SB602 White Spray</strong> for PU foam-to-foam and fabric upholstery bonding. Use <strong>Synthetic Rubber Adhesive</strong> for brush/spreader lamination of Formica, plywood, and wood.</p>",
    faqs=[
        {"question": "What is the difference between standard SBS Spray and SB602 White?", "answer": "SB602 is pigmented white for high visibility on light-colored foam and upholstery fabrics, preventing over-spraying and bleed-through."},
        {"question": "Does SBS spray adhesive stay soft on foam joints?", "answer": "Yes, it cures to a flexible, non-hardening bond line that preserves the natural softness of PU foam mattresses and cushions."}
    ]
)

cat_hardware = Category.objects.create(
    name="Hardware",
    slug="hardware",
    meta_title="Silicone Sealants, Super Glue & Spray Paint | Uniworld",
    meta_description="Acetic and neutral silicone sealants, nail-free adhesive, super glue, aerosol spray paint and rat glue for hardware stores, trade and DIY across Bangladesh.",
    h1_title="Hardware Sealants, Glues & Spray Paint",
    content="<p>Complete trade, glazing, construction, and retail hardware range manufactured to ISO 9001:2015 standards. Includes fast-curing Acetic and Neutral Cure 300ml silicone cartridges, heavy-duty Nail Free construction adhesive, instant cyanoacrylate super glue, 400ml fast-drying aerosol spray paints, and high-tack rodent glue traps.</p>",
    buying_guide="<p><strong>How to choose:</strong> Use <strong>Acetic Silicone</strong> for glass and bathroom tiles, and <strong>Neutral Silicone</strong> for mirrors, coated aluminium, and stone. Use <strong>Nail Free Sealant</strong> for mounting skirting, panels, and mouldings without drilling.</p>",
    faqs=[
        {"question": "Can I use Acetic Silicone Sealant on mirrors?", "answer": "No. Acetic silicone releases acetic acid during curing which can corrode mirror silvering. Always use Uniworld Neutral Cure Silicone Sealant for mirrors and metals."},
        {"question": "How much weight can Nail Free Sealant hold?", "answer": "Once fully cured in 24–48 hours, Nail Free Sealant supports heavy architectural trims, wood panels, and PVC profiles without mechanical fasteners."}
    ]
)

# 2. Create Industries
ind_footwear = Industry.objects.create(name="Footwear & Leather Goods", slug="footwear-leather")
ind_furniture = Industry.objects.create(name="Woodworking & Furniture", slug="woodworking-furniture")
ind_hardware = Industry.objects.create(name="DIY, Trade & Hardware", slug="hardware-construction")
ind_auto = Industry.objects.create(name="Automotive & Foam", slug="automotive-foam")

# 3. Create All 15 Real Products from Audit Report
products_data = [
    {
        "name": "SBS Sprayable Adhesive",
        "slug": "sbs-sprayable-adhesive",
        "meta_title": "SBS Sprayable Adhesive for Furniture & Foam | Uniworld",
        "meta_description": "SBS spray adhesive with fast tack and a flexible, durable bond for furniture, foam and general industrial work. For manual or semi-auto lines. 3 L and 15 L.",
        "h1_title": "SBS Sprayable Adhesive for Furniture & Foam",
        "category": cat_furniture,
        "industry": ind_furniture,
        "is_featured": True,
        "img": "product/images/product/01.png",
        "sizes": "3 L Tin\n15 L Pail\n200 L Drum",
        "description": "Uniworld SBS Sprayable Adhesive is a fast-tack styrene-butadiene-styrene (SBS) solvent-based spray adhesive engineered for PU foam lamination, sofa upholstery, mattress assembly, and general woodworking.",
        "applications": "PU foam to foam, foam to wood/plywood, fabric and non-woven upholstery, acoustic panels, and automotive headliners.",
        "features": "Fast initial grab within 60–90 seconds\nSmooth, clog-free spray atomization with low overspray\nRemains permanently flexible without hardening foam joints\nCompatible with manual and semi-automatic spray guns",
        "how_to_apply": "Ensure foam and substrate surfaces are clean, dry, and dust-free.\nAdjust spray gun nozzle pressure to 3–4 bar and apply an even coat to both bonding surfaces.\nAllow 2–5 minutes open flash-off time until tacky to the touch.\nAlign and press surfaces firmly together with uniform hand or roller pressure.",
        "tech_specs": {
            "Chemistry Base": "Styrene-Butadiene-Styrene (SBS)",
            "Colour": "Light Amber / Clear",
            "Brookfield Viscosity (25°C)": "80 – 120 cPs",
            "Open Tack Time": "2 – 5 minutes",
            "Full Cure Time": "12 – 24 hours",
            "Service Temperature": "-10°C to +65°C",
            "Pack Sizes": "3 L, 15 L, 200 L",
            "Shelf Life": "12 Months (sealed below 30°C)"
        },
        "faqs": [
            {"question": "What is the difference between standard SBS Sprayable Adhesive and SB602 White?", "answer": "Standard SBS Sprayable Adhesive dries clear/amber for general foam and wood bonding, whereas SB602 is pigmented white so operators can clearly see spray coverage on light upholstery fabrics."},
            {"question": "What spray nozzle size works best?", "answer": "A 1.5 mm to 2.0 mm gravity or pressure-feed spray nozzle at 3–4 bar air pressure delivers optimal atomization."}
        ]
    },
    {
        "name": "SB602 White SBS Spray Adhesive",
        "slug": "sbs-sprayable-adhesive-white-sb602",
        "meta_title": "SB602 White SBS Spray Adhesive | Uniworld",
        "meta_description": "SB602 is Uniworld's white SBS sprayable adhesive for fast, strong and reliable bonding across a wide range of materials. Request a quote for bulk supply.",
        "h1_title": "SB602 White SBS Spray Adhesive",
        "category": cat_furniture,
        "industry": ind_furniture,
        "is_featured": True,
        "img": "product/images/product/01.png",
        "sizes": "3 L Tin\n15 L Pail",
        "description": "SB602 is Uniworld's white-pigmented styrene-butadiene-styrene (SBS) sprayable adhesive formulated for high-visibility coverage on light-colored PU foam, mattress ticking, and upholstery fabrics.",
        "applications": "Mattress manufacturing, light-colored sofa upholstery, EPE/PU foam lamination, fabric-to-wood panels, and packaging foam.",
        "features": "White pigment makes spray pattern clearly visible to prevent missed spots\nZero yellow staining or bleed-through on white fabrics\nHigh immediate tack for rapid assembly lines\nSoft, flexible bond line",
        "how_to_apply": "Stir well before transferring into the spray tank.\nSpray evenly across both foam and fabric/wood substrates from 20–25 cm distance.\nWait 2–6 minutes for solvent evaporation.\nPress substrates firmly together; full bond develops over 24 hours.",
        "tech_specs": {
            "Chemistry Base": "Pigmented Styrene-Butadiene-Styrene (SBS)",
            "Colour": "Opaque White",
            "Brookfield Viscosity (25°C)": "90 – 140 cPs",
            "Open Tack Time": "2 – 6 minutes",
            "Full Cure Time": "12 – 24 hours",
            "Service Temperature": "-10°C to +65°C",
            "Pack Sizes": "3 L, 15 L",
            "Shelf Life": "12 Months"
        },
        "faqs": [
            {"question": "Why choose SB602 White over clear SBS spray adhesive?", "answer": "SB602 provides visual spray control on white foam and pale upholstery textiles while preventing dark shadow lines under thin fabrics."}
        ]
    },
    {
        "name": "Polyurethane (PU) Adhesive",
        "slug": "polyurethane-adhesive",
        "meta_title": "Polyurethane (PU) Adhesive, High Strength | Uniworld",
        "meta_description": "High-strength polyurethane adhesive that holds under stress, heat and moisture. For footwear, furniture, construction and general manufacturing. 3 L and 15 L.",
        "h1_title": "Polyurethane (PU) Adhesive",
        "category": cat_footwear,
        "industry": ind_footwear,
        "is_featured": True,
        "img": "product/images/product/single01.png",
        "sizes": "3 L Tin\n15 L Pail",
        "description": "Uniworld Polyurethane (PU) Adhesive is a crystal-clear, heat-activated solvent-based polyurethane formulation engineered for high-strength bonding of PU, PVC, synthetic leather, and rubber footwear components.",
        "applications": "Shoe sole-to-upper bonding (PVC, PU, TR, leather, Rexine), bag and belt manufacturing, and PVC membrane lamination.",
        "features": "Crystal-clear bond line that never yellows light uppers\nHigh peel strength (4.1 N/mm) and water resistance\nReactivates cleanly at 60°C–70°C\nCompatible with isocyanate hardeners for two-component performance",
        "how_to_apply": "Clean PU/PVC soles with Uniworld Synthetic Cleaner and apply PU/PVC Primer.\nApply one uniform brush coat of PU Adhesive to both sole and upper.\nDry for 10–15 minutes until completely tack-free.\nHeat-activate at 60°C–70°C for 10–15 seconds and press firmly.",
        "tech_specs": {
            "Chemistry Base": "Polyurethane (PU)",
            "Colour": "Crystal Clear",
            "Brookfield Viscosity (25°C)": "2,000 – 2,400 cPs",
            "Peel Strength (24h)": "4.1 N/mm",
            "Heat Activation Temp": "60°C – 70°C",
            "Heat Resistance": "Up to 70°C",
            "Pack Sizes": "3 L, 15 L",
            "Shelf Life": "12 Months"
        },
        "faqs": [
            {"question": "When should I choose Standard PU vs. Premium PU Adhesive?", "answer": "Standard PU (4.1 N/mm peel strength) is ideal for daily domestic footwear and leather goods. Upgrade to Premium PU (5.2 N/mm) for export shoes or extreme tropical heat up to 85°C."}
        ]
    },
    {
        "name": "Premium Polyurethane (PU) Adhesive",
        "slug": "polyurethane-adhesive-premium",
        "meta_title": "Premium Polyurethane (PU) Adhesive | Uniworld",
        "meta_description": "Uniworld's highest-performance PU adhesive, with superior bond strength, durability and heat and moisture resistance for the most demanding production work.",
        "h1_title": "Premium Polyurethane (PU) Adhesive",
        "category": cat_footwear,
        "industry": ind_footwear,
        "is_featured": True,
        "img": "product/images/product/single01.png",
        "sizes": "3 L Tin\n15 L Pail",
        "description": "Uniworld Premium Polyurethane (PU) Adhesive is our highest-solid, maximum-strength PU formulation built for export-grade footwear, heavy-duty industrial boots, and high-heat environments.",
        "applications": "Export leather and synthetic footwear, sports shoes, Phylon/EVA/PU outsoles, and marine or high-humidity vinyl bonding.",
        "features": "Peak 24-hour peel strength of 5.2 N/mm\nSuperior tropical heat and hydrolysis resistance up to 85°C\nNon-yellowing transparent bond line\nOutstanding flex-crack endurance",
        "how_to_apply": "Degrease soles with Synthetic Cleaner and prime with EVA Primer or PU/PVC Primer.\nBrush an even layer onto both surfaces and allow 12–18 minutes drying.\nReactivate in a heat tunnel at 65°C–75°C and press immediately under 3–4 bar pressure.",
        "tech_specs": {
            "Chemistry Base": "High-Solid Polyurethane (PU)",
            "Colour": "Crystal Clear",
            "Brookfield Viscosity (25°C)": "2,400 – 2,800 cPs",
            "Peel Strength (24h)": "5.2 N/mm",
            "Heat Activation Temp": "65°C – 75°C",
            "Heat Resistance": "Up to 85°C",
            "Pack Sizes": "3 L, 15 L",
            "Shelf Life": "12 Months"
        },
        "faqs": [
            {"question": "Can Premium PU Adhesive be mixed with a crosslinking hardener?", "answer": "Yes, adding 3–5% isocyanate hardener further increases heat resistance above 90°C for export footwear standards."}
        ]
    },
    {
        "name": "Graft CR Adhesive (Grafted Chloroprene)",
        "slug": "graft-adhesive",
        "meta_title": "Graft CR (Chloroprene) Adhesive for Footwear | Uniworld",
        "meta_description": "Grafted chloroprene (CR) adhesive with fast initial tack and high final strength. Holds up to stress, temperature change and vibration on many substrates.",
        "h1_title": "Graft CR Adhesive (Grafted Chloroprene)",
        "category": cat_footwear,
        "industry": ind_footwear,
        "is_featured": True,
        "img": "product/images/product/single04.png",
        "sizes": "3 L Tin\n15 L Pail",
        "description": "Uniworld Graft CR Adhesive is a methyl-methacrylate grafted polychloroprene adhesive formulated to bond difficult, low-surface-energy substrates such as EVA, TPR, vulcanized rubber, and leather.",
        "applications": "EVA and Phylon midsoles, TPR outsoles, natural and synthetic rubber, canvas, leather uppers, and PVC trim.",
        "features": "Chemically grafted polymer backbone for superior adhesion on EVA & TPR\nAggressive green tack with 4.6 N/mm final peel strength\nExcellent resistance to flexing, vibration, and temperature swings\nWorks via cold contact or mild heat activation",
        "how_to_apply": "Prime EVA soles with Uniworld EVA Primer and allow 3–5 minutes to dry.\nApply a uniform coat of Graft CR Adhesive to both surfaces.\nAllow 10–20 minutes open drying time, warm briefly at 55°C–60°C if needed, and press firmly.",
        "tech_specs": {
            "Chemistry Base": "Grafted Polychloroprene (Graft CR)",
            "Colour": "Milky / Pale Yellow",
            "Brookfield Viscosity (25°C)": "2,800 – 3,400 cPs",
            "Peel Strength (24h)": "4.6 N/mm",
            "Open Tack Time": "10 – 20 minutes",
            "Heat Resistance": "Up to 75°C",
            "Pack Sizes": "3 L, 15 L",
            "Shelf Life": "12 Months"
        },
        "faqs": [
            {"question": "Do I still need EVA Primer when using Graft CR Adhesive?", "answer": "For molded EVA and Phylon soles, applying Uniworld EVA Primer first ensures maximum cross-linked adhesion and eliminates edge lifting."}
        ]
    },
    {
        "name": "Synthetic Rubber Adhesive",
        "slug": "synthetic-rubber-adhesive",
        "meta_title": "Synthetic Rubber Adhesive for Footwear & Foam | Uniworld",
        "meta_description": "High-tack synthetic rubber adhesive for footwear, foam lamination and furniture. Strong initial grab and a flexible bond that resists cracking and peeling.",
        "h1_title": "Synthetic Rubber Adhesive",
        "category": cat_footwear,
        "industry": ind_furniture,
        "is_featured": True,
        "img": "product/images/product/single02.png",
        "sizes": "3 L Tin\n15 L Pail",
        "description": "Uniworld Synthetic Rubber Adhesive is a heavy-bodied polychloroprene (CR) multipurpose contact adhesive delivering strong immediate grab and durable flexibility across leather, foam, wood, laminate, and rubber.",
        "applications": "Footwear lasting and insole bonding, HPL/Formica lamination on plywood, leather goods, rubber sheets, and metal trim.",
        "features": "High solid viscosity (3,500–4,500 cPs) prevents soaking into porous wood or leather\nLong 15–25 minute open tack window for large panels\nWaterproof, flexible bond that resists cracking\nEasy brush or notched-trowel application",
        "how_to_apply": "Clean both surfaces of dust, oil, and moisture.\nApply an even coat to both substrates using a brush or serrated spreader.\nWait 15–25 minutes until solvents evaporate and the film feels dry-tacky.\nPosition carefully (bond is instant on contact) and roll firmly.",
        "tech_specs": {
            "Chemistry Base": "Polychloroprene (Synthetic Rubber)",
            "Colour": "Light Yellow / Amber",
            "Brookfield Viscosity (25°C)": "3,500 – 4,500 cPs",
            "Open Tack Time": "15 – 25 minutes",
            "Full Cure Time": "24 hours",
            "Heat Resistance": "Up to 70°C",
            "Pack Sizes": "3 L, 15 L",
            "Shelf Life": "12 Months"
        },
        "faqs": [
            {"question": "Can Synthetic Rubber Adhesive be used for Formica and plywood?", "answer": "Yes, its high viscosity and long open tack time make it ideal for bonding HPL/Formica laminates to plywood and MDF."}
        ]
    },
    {
        "name": "PU/PVC Primer",
        "slug": "pupvc-primer",
        "meta_title": "PU/PVC Primer for Synthetic Leather & Rexine | Uniworld",
        "meta_description": "Surface primer that strengthens adhesive bonds on PU, PVC, Rexine and synthetic leather, improving durability and reducing the risk of delamination.",
        "h1_title": "PU/PVC Primer for Synthetic Leather",
        "category": cat_footwear,
        "industry": ind_footwear,
        "is_featured": False,
        "img": "product/images/product/single03.png",
        "sizes": "1 L Bottle\n3 L Tin\n15 L Pail",
        "description": "Uniworld PU/PVC Primer is a specialized surface-activation primer formulated to prepare smooth polyurethane, PVC, and Rexine surfaces for maximum adhesion with Uniworld PU adhesives.",
        "applications": "Molded PVC outsoles, PU soles, synthetic leather uppers, Rexine, and coated footwear components.",
        "features": "Etches and chemically activates smooth synthetic surfaces\nPrevents plasticizer migration and sole delamination\nFast 3–5 minute flash-off drying time\nCrystal-clear non-staining formula",
        "how_to_apply": "Wipe the PU/PVC sole first with Uniworld Synthetic Cleaner.\nApply a thin, uniform coat of PU/PVC Primer using a clean brush.\nAllow 3–5 minutes to dry completely before applying Polyurethane (PU) Adhesive.",
        "tech_specs": {
            "Chemistry Base": "Solvent-Based Adhesion Promoter",
            "Colour": "Crystal Clear",
            "Viscosity (25°C)": "< 50 cPs (Water-thin)",
            "Drying Time": "3 – 5 minutes",
            "Compatible Adhesives": "PU Adhesive, Premium PU Adhesive",
            "Pack Sizes": "1 L, 3 L, 15 L",
            "Shelf Life": "12 Months"
        },
        "faqs": [
            {"question": "Which adhesive should I apply after PU/PVC Primer?", "answer": "Apply Uniworld Polyurethane (PU) Adhesive or Premium PU Adhesive once the primer has dried for 3–5 minutes."}
        ]
    },
    {
        "name": "EVA Primer",
        "slug": "eva-primer",
        "meta_title": "EVA Primer for Footwear & Foam Bonding | Uniworld",
        "meta_description": "Adhesion promoter that activates EVA surfaces for stronger bonds with solvent- or water-based adhesives in footwear, leather goods and foam applications.",
        "h1_title": "EVA Primer for Footwear & Foam",
        "category": cat_footwear,
        "industry": ind_footwear,
        "is_featured": False,
        "img": "product/images/product/single03.png",
        "sizes": "1 L Bottle\n3 L Tin\n15 L Pail",
        "description": "Uniworld EVA Primer is a fast-acting surface primer that modifies non-porous EVA and Phylon foam surfaces so PU and Graft CR adhesives achieve deep structural bonding.",
        "applications": "Injection-molded EVA soles, Phylon midsoles, EVA sandals/slippers, and closed-cell EVA foam sheets.",
        "features": "Transforms low-surface-energy EVA for high-peel bonding\nEliminates buffing/roughing steps on many EVA grades\nCompatible with both Graft CR and PU adhesive systems\nDries in 3–5 minutes",
        "how_to_apply": "Clean EVA soles with Synthetic Cleaner to remove mould-release wax.\nBrush a single thin coat of EVA Primer across the bonding area.\nAllow 3–5 minutes drying time (or brief UV/heat tunnel pass), then apply Graft CR or Premium PU Adhesive.",
        "tech_specs": {
            "Chemistry Base": "Halogenated / Polymeric Primer",
            "Colour": "Clear",
            "Viscosity (25°C)": "< 50 cPs",
            "Drying Time": "3 – 5 minutes",
            "Compatible Adhesives": "Graft CR Adhesive, Premium PU Adhesive",
            "Pack Sizes": "1 L, 3 L, 15 L",
            "Shelf Life": "9 Months (store in cool dark place)"
        },
        "faqs": [
            {"question": "Can EVA Primer be used with Graft CR Adhesive?", "answer": "Yes, Uniworld EVA Primer is formulated to work seamlessly with both Graft CR Adhesive and Premium PU Adhesive."}
        ]
    },
    {
        "name": "Synthetic Cleaner",
        "slug": "synthetic-cleaner",
        "meta_title": "Synthetic Cleaner for PU & PVC Soles | Uniworld",
        "meta_description": "Fast-evaporating solvent cleaner that lifts dust, grease and mould-release residue from PU and PVC soles and uppers before bonding, for streak-free prep.",
        "h1_title": "Synthetic Cleaner for PU & PVC Soles",
        "category": cat_footwear,
        "industry": ind_footwear,
        "is_featured": False,
        "img": "product/images/product/single03.png",
        "sizes": "1 L Bottle\n3 L Tin\n15 L Pail",
        "description": "Uniworld Synthetic Cleaner is a fast-evaporating industrial solvent cleaner designed to remove silicone mould-release agents, oil, wax, and dust from PU, PVC, and rubber shoe soles prior to priming.",
        "applications": "Pre-bond cleaning of PU soles, PVC soles, TPR, synthetic leather uppers, and rubber components.",
        "features": "Dissolves silicone mould-release residue completely\nEvaporates in 1–2 minutes leaving zero oily film\nPrevents premature bond failure caused by surface contamination\nSafe on most footwear synthetics",
        "how_to_apply": "Moisten a clean lint-free cotton cloth with Synthetic Cleaner.\nWipe the sole or upper bonding surface thoroughly in one direction.\nAllow 1–2 minutes flash-off evaporation before applying EVA Primer or PU/PVC Primer.",
        "tech_specs": {
            "Chemistry Base": "Precision Solvent Blend",
            "Colour": "Water-Clear",
            "Flash-Off Time": "1 – 2 minutes",
            "Residue": "Zero (100% volatile)",
            "Pack Sizes": "1 L, 3 L, 15 L",
            "Shelf Life": "18 Months"
        },
        "faqs": [
            {"question": "Why is cleaning soles before priming important?", "answer": "Injection-molded PU and PVC soles carry invisible silicone release agents that block primer and adhesive penetration unless wiped with Synthetic Cleaner first."}
        ]
    },
    {
        "name": "Acetic Silicone Sealant",
        "slug": "silicone-sealant",
        "meta_title": "Acetic Silicone Sealant, Clear & White 300 ml | Uniworld",
        "meta_description": "Fast-curing acetic silicone sealant for glass, aluminium, tiles and bathrooms. Weatherproof and UV-resistant; the white is mould-resistant. 300 ml cartridge.",
        "h1_title": "Acetic Silicone Sealant (Clear & White)",
        "category": cat_hardware,
        "industry": ind_hardware,
        "is_featured": True,
        "img": "product/images/product/single03.png",
        "sizes": "300 ml Cartridge (24 pcs/carton)",
        "description": "Uniworld Acetic Silicone Sealant is a fast-curing, one-component acetoxy silicone sealant engineered for glass window glazing, ceramic bathroom tiles, shower enclosures, and non-porous aluminium joints.",
        "applications": "Glass-to-glass and glass-to-aluminium glazing, sanitary ware, bathtubs, kitchen sinks, ceramic tiles, and aquariums.",
        "features": "Fast 10-minute tack-free skin formation\n100% weatherproof and UV-resistant for indoor/outdoor joints\nWhite grade contains anti-fungal mould-resistant additives\nPermanently elastic (±25% joint movement capability)",
        "how_to_apply": "Clean and dry joint edges; mask adjacent surfaces with painter's tape.\nCut cartridge nozzle at a 45° angle to match joint width (3–12 mm).\nExtrude smoothly with a caulking gun and tool within 5 minutes before skinning.\nRemove masking tape immediately; full cure in 24 hours.",
        "tech_specs": {
            "Chemistry Base": "Acetoxy Cure Silicone",
            "Available Colours": "Clear, White, Black",
            "Tack-Free Time": "8 – 12 minutes",
            "Full Cure Rate": "2–3 mm per 24 hours",
            "Service Temperature": "-40°C to +150°C",
            "Cartridge Volume": "300 ml",
            "Shelf Life": "12 Months"
        },
        "faqs": [
            {"question": "Where should I use Acetic vs. Neutral Silicone Sealant?", "answer": "Use Acetic Silicone for glass, glazed tiles, and bathrooms. For mirrors, galvanized steel, coated aluminium, concrete, and marble, use Uniworld Neutral Cure Silicone Sealant."}
        ]
    },
    {
        "name": "Neutral Cure Silicone Sealant",
        "slug": "silicone-sealant-neutral",
        "meta_title": "Neutral Cure Silicone Sealant | Uniworld",
        "meta_description": "One-component neutral cure silicone sealant for durable, flexible, long-lasting sealing. Made in Bangladesh by Uniworld. Request a quote for bulk supply.",
        "h1_title": "Neutral Cure Silicone Sealant",
        "category": cat_hardware,
        "industry": ind_hardware,
        "is_featured": False,
        "img": "product/images/product/single03.png",
        "sizes": "300 ml Cartridge (24 pcs/carton)",
        "description": "Uniworld Neutral Cure Silicone Sealant is a non-corrosive, low-odor oxime silicone sealant safe for mirrors, coated metals, uPVC window frames, concrete, and natural stone.",
        "applications": "Mirror installation, uPVC and powder-coated aluminium doors/windows, ACP cladding joints, marble/granite, and galvanized steel.",
        "features": "Non-corrosive neutral cure—will not damage mirror silvering or metals\nVirtually odorless application indoors\nStrong primerless adhesion to masonry, uPVC, glass, and metal\nUV, ozone, and rain resistant",
        "how_to_apply": "Ensure substrates are clean, dry, and free of loose dust.\nApply continuously into the joint using a standard 300ml caulking gun.\nTool smooth within 10 minutes; cures fully in 24–48 hours.",
        "tech_specs": {
            "Chemistry Base": "Neutral Oxime Silicone",
            "Available Colours": "Clear, White, Grey, Black",
            "Tack-Free Time": "12 – 18 minutes",
            "Full Cure Rate": "2 mm per 24 hours",
            "Service Temperature": "-40°C to +150°C",
            "Cartridge Volume": "300 ml",
            "Shelf Life": "12 Months"
        },
        "faqs": [
            {"question": "Is Neutral Cure Silicone safe for fixing mirrors?", "answer": "Yes. Unlike acetic silicone, Neutral Cure Silicone does not release acid and will not corrode or blacken mirror backings."}
        ]
    },
    {
        "name": "Nail Free Sealant",
        "slug": "nail-free-sealant",
        "meta_title": "Nail Free Sealant (No More Nails Adhesive) | Uniworld",
        "meta_description": "High-strength construction adhesive that replaces nails, screws and drilling in most fixing applications. No drilling, no dust and no damaged walls.",
        "h1_title": "Nail Free Sealant: No More Nails Adhesive",
        "category": cat_hardware,
        "industry": ind_hardware,
        "is_featured": False,
        "img": "product/images/product/single03.png",
        "sizes": "300 ml Cartridge",
        "description": "Uniworld Nail Free Sealant is a heavy-duty synthetic polymer construction adhesive designed to replace nails, screws, and wall plugs when mounting panels, mouldings, skirting, and fixtures.",
        "applications": "Wooden skirting boards, PVC wall panels, gypsum cornices, WPC louvers, window sills, metal signs, and ceramic tiles.",
        "features": "High initial grab holds vertical panels without slipping\nEliminates drilling noise, dust, and cracked walls\nBridges minor gaps on uneven plaster or brick surfaces\nPaintable once cured",
        "how_to_apply": "Apply zig-zag beads (4–6 mm wide) onto the back of the panel or trim.\nPress firmly onto the wall, pull away for 30 seconds to flash off solvent, then press back firmly.\nSupport heavy vertical items for 12–24 hours until full structural strength is reached.",
        "tech_specs": {
            "Chemistry Base": "High-Grab Synthetic Rubber / Resin",
            "Colour": "Beige / Off-White",
            "Initial Grab": "Instant tack (30 sec flash-off)",
            "Full Cure Time": "24 – 48 hours",
            "Cartridge Volume": "300 ml",
            "Shelf Life": "12 Months"
        },
        "faqs": [
            {"question": "Does Nail Free Sealant work on painted walls and concrete?", "answer": "Yes, provided the paint layer is sound and free from loose chalking or dust."}
        ]
    },
    {
        "name": "Cyanoacrylate Super Glue",
        "slug": "cyanoacrylate-super-glue",
        "meta_title": "Cyanoacrylate Super Glue, Instant Bond | Uniworld",
        "meta_description": "Uniworld super glue cures in seconds for a strong, lasting bond on most materials. Precision nozzle for clean, controlled use in DIY, crafts and repairs.",
        "h1_title": "Cyanoacrylate Super Glue",
        "category": cat_hardware,
        "industry": ind_hardware,
        "is_featured": False,
        "img": "product/images/product/single03.png",
        "sizes": "3 g Tube\n20 g Bottle\n50 g Bottle",
        "description": "Uniworld Cyanoacrylate Super Glue is a fast-acting ethyl cyanoacrylate instant adhesive that bonds non-porous surfaces within 5 to 15 seconds.",
        "applications": "Hard plastics (ABS, PVC, acrylic), rubber O-rings, metal hardware, ceramic repairs, wood crafts, and leather accessories.",
        "features": "Cures in 5–15 seconds at room temperature\nPrecision anti-clog applicator nozzle for pinpoint drops\nCrystal-clear invisible joint\nNote: Not recommended for polyethylene (PE), polypropylene (PP), or Teflon",
        "how_to_apply": "Ensure mating parts fit tightly and are clean and dry.\nApply a single small drop to one surface only.\nPress parts together firmly for 10–15 seconds. Avoid skin contact.",
        "tech_specs": {
            "Chemistry Base": "Ethyl Cyanoacrylate",
            "Colour": "Water-Clear",
            "Fixture Time": "5 – 15 seconds",
            "Full Cure Time": "12 hours",
            "Pack Sizes": "3 g, 20 g, 50 g",
            "Shelf Life": "12 Months (store cool & dry)"
        },
        "faqs": [
            {"question": "Which plastics will Cyanoacrylate Super Glue not bond?", "answer": "Standard cyanoacrylate does not bond oily low-energy plastics such as polyethylene (PE), polypropylene (PP), or PTFE without a polyolefin primer."}
        ]
    },
    {
        "name": "Aerosol Spray Paint",
        "slug": "aerosol-spray-paint",
        "meta_title": "Aerosol Spray Paint 400 ml, Fast Drying | Uniworld",
        "meta_description": "Fast-drying aerosol spray paint with even colour and strong coverage on metal, wood and plastic. 400 ml can for DIY, repairs and hardware work.",
        "h1_title": "Aerosol Spray Paint (400 ml)",
        "category": cat_hardware,
        "industry": ind_hardware,
        "is_featured": False,
        "img": "product/images/product/01.png",
        "sizes": "400 ml Aerosol Can (12 cans/carton)",
        "description": "Uniworld Aerosol Spray Paint is a fast-drying acrylic-modified alkyd spray coating engineered for smooth, high-gloss or matte finishes on metal, wood, machinery, and plastics.",
        "applications": "Metal gates and grilles, automotive touch-ups, wooden furniture, PVC pipes, industrial machinery, and DIY crafts.",
        "features": "Touch-dry in 10 minutes; recoatable after 15 minutes\nSmooth fan-spray valve prevents drips and runs\nHigh pigment opacity covers ~1.5–2.0 m² per 400 ml can\nAvailable in Gloss Black, Gloss White, Clear Lacquer, Red, Silver, Gold & industrial colours",
        "how_to_apply": "Sand and clean surface of rust, oil, and loose paint.\nShake the 400 ml can vigorously for 60 seconds until the mixing ball rattles freely.\nSpray in thin sweeping passes from 20–25 cm away; apply 2–3 light coats 15 minutes apart.",
        "tech_specs": {
            "Chemistry Base": "Acrylic-Modified Alkyd",
            "Can Volume": "400 ml",
            "Coverage": "1.5 – 2.0 m² per can (2 coats)",
            "Touch Dry Time": "10 minutes (25°C)",
            "Recoat Window": "15 – 20 minutes",
            "Shelf Life": "24 Months"
        },
        "faqs": [
            {"question": "How many square meters does one 400 ml can cover?", "answer": "One 400 ml can covers approximately 1.5 to 2.0 square meters with two even coats."}
        ]
    },
    {
        "name": "Rat Glue",
        "slug": "rat-glue",
        "meta_title": "Rat Glue, High-Tack Rodent Trap Adhesive | Uniworld",
        "meta_description": "Ready-to-use, high-viscosity rat glue with strong tack and a long-lasting hold for catching rats, mice, lizards and other crawling pests.",
        "h1_title": "Rat Glue: High-Tack Rodent Trap Adhesive",
        "category": cat_hardware,
        "industry": ind_hardware,
        "is_featured": False,
        "img": "product/images/product/single02.png",
        "sizes": "135 g Tube\n400 g Tin\n1 kg Tin",
        "description": "Uniworld Rat Glue is a non-toxic, ultra-high-viscosity polybutene rodent trap adhesive that stays permanently tacky without drying out to capture rats, mice, and crawling pests.",
        "applications": "Warehouses, food storage facilities, grain mills, commercial kitchens, retail shops, and residential pest control.",
        "features": "Non-drying, non-toxic formula (contains no rodenticide poison)\nExtreme tack holds large rats and mice securely\nEffective across both hot summer and cool winter temperatures\nEasy to spread on cardboard, plywood, or plastic trays",
        "how_to_apply": "Spread a 3–5 mm thick layer onto heavy cardboard or a wooden board (approx. 20×30 cm).\nPlace a small piece of bait in the center and position boards along walls where rodent droppings appear.\nKeep out of reach of children and household pets; use vegetable oil to clean accidental skin contact.",
        "tech_specs": {
            "Chemistry Base": "High-Viscosity Polybutene Polymer",
            "Toxicity": "Non-Toxic / Poison-Free",
            "Operating Temp": "5°C to 50°C",
            "Pack Sizes": "135 g Tube, 400 g Tin, 1 kg Tin",
            "Shelf Life": "24 Months"
        },
        "faqs": [
            {"question": "How do I remove Rat Glue if it accidentally touches skin or floor?", "answer": "Apply ordinary vegetable cooking oil or baby oil to dissolve the adhesive, wipe clean with a cloth, and wash with soap and warm water."}
        ]
    }
]

for item in products_data:
    img_path = item.pop("img")
    p = Product.objects.create(**item)
    ProductImage.objects.create(product=p, image=img_path, is_primary=True, order=0)

Contact.objects.create(
    company_name="Uniworld Adhesives",
    factory_address="Dhaka-Sylhet Highway,\nMahona, Rupganj,\nNarayanganj",
    head_office_address="Family World Tower,\n2/6 Sir Syed Road,\nAsad Gate, Dhaka 1207",
    phone="+880 1898-802405",
    phone_2="+880 1711-563790",
    phone_3="+880 1757-692826",
    email="info@uniworldsolutions.com",
    working_hours="Saturday – Thursday, 9:00 AM – 6:00 PM",
    facebook_url="https://www.facebook.com/uniworldadhesive",
    is_active=True
)

print(f"Successfully seeded {Category.objects.count()} categories and {Product.objects.count()} real products!")