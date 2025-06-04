import math
import psycopg2

# --- 1) DOMSOI Factor Mapping ---
# Mapping FAO soil unit codes to seismic amplification factors based on NEHRP site classes
DOMSOI_FACTOR_MAPPING = {}
# Site Class A: Rock/Hard Soil
DOMSOI_FACTOR_MAPPING.update(dict.fromkeys(["I","RK","GL","WR"], 0.8))
# Site Class B: Firm Soil
DOMSOI_FACTOR_MAPPING.update(dict.fromkeys(["J","Je","Jc","Jd","Jt","Qa","Ql","Qf","Qe","U"], 0.9))
# Site Class C: Dense Soil/Soft Rock
DOMSOI_FACTOR_MAPPING.update(dict.fromkeys([
    "Be","Bd","Bh","Bg","Bx","Bk","Bc","Bv","Bf",
    "Ch","Ck","Cl","Cg",
    "Lc","Lo","Lv","Lf","La","Lp","Lk",
    "Vp","Vc",
    "Rx","Rc","Rd","Re"
], 1.2))
# Site Class D: Stiff Soil
DOMSOI_FACTOR_MAPPING.update(dict.fromkeys([
    "De","Dd","Dg","Fa","Fp","Fr","Fo","Fx","Fh",
    "Hh","Hc","Hl","Hg","Zg"
], 1.5))
# Site Class E: Soft Soil/Clay
DOMSOI_FACTOR_MAPPING.update(dict.fromkeys(["O","Od","Oe"], 2.4))

# --- 2) Soil Amplification ---
def get_soil_amplification(lat, lon):
    conn = psycopg2.connect(dbname="postgis_35_sample", user="postgres", password="1234", host="localhost", port="5432")
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT domsoi
            FROM soils
            ORDER BY ST_DistanceSphere(
                ST_SetSRID(ST_MakePoint(%s,%s),4326), wkb_geometry
            ) LIMIT 1;
            """, (lon, lat)
        )
        row = cur.fetchone()
    finally:
        cur.close()
        conn.close()
    if not row:
        return 1.0,1.0,1.0,None,1.0
    soil_code = row[0]
    factor = DOMSOI_FACTOR_MAPPING.get(soil_code,1.0)
    return factor,factor,factor,soil_code,factor

# --- 3) Slip‑Type Severity ---
SLIP_FACTOR_MAPPING = {
    "Blind Thrust":1.3, "Subduction Thrust":1.4, "Reverse":1.2,
    "Reverse-Dextral":1.2, "Reverse-Strike-Slip":1.2, "Thrust":1.3,
    "Strike-Slip":1.0, "Dextral":1.0, "Sinistral":1.0,
    "Normal":0.9, "Normal-Sinistral":0.9, "Normal-Strike-Slip":0.9,
    "Spreading Ridge":0.8, None:1.0
}

def get_slip_factor(slip): return SLIP_FACTOR_MAPPING.get(slip,1.0)

# --- 4) Fault Info ---
def get_fault_info(lat, lon):
    conn = psycopg2.connect(dbname="postgis_35_sample", user="postgres", password="1234", host="localhost", port="5432")
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT slip_type, net_slip_rate, ST_DistanceSphere(
                ST_SetSRID(ST_MakePoint(%s,%s),4326), wkb_geometry
            ) as dist_m
            FROM fault_lines ORDER BY dist_m LIMIT 1;
            """, (lon, lat)
        )
        row = cur.fetchone()
    finally:
        cur.close()
        conn.close()
    if not row: return None,None,None
    slip_type, net_slip, dist_m = row
    # Parse net_slip robustly
    avg_slip = 1.0
    if isinstance(net_slip, str):
        parts = [p for p in net_slip.strip('() ').split(',') if p]
        try:
            avg_slip = float(parts[1] if len(parts)>1 else parts[0])
        except Exception:
            avg_slip = 1.0
    # Convert m->km
    return dist_m/1000.0, slip_type, avg_slip

# --- 5) Radius Formula ---
def base_radius(mag, depth, fault_dist=None):
    """
    Computes the base rupture radius (in km) given magnitude and depth.
    Ignores fault distance attenuation to model source radius directly.
    """
    # Attenuation scale for depth only
    depth_scale = 15.0
    decay = depth / depth_scale
    R0 = (10 ** (0.5 * mag - 1.8)) * math.exp(-decay)
    return R0

def calculate_radii(mag, depth, fdist, slip, avg_slip, sw, sm, sb, df):
    R0 = base_radius(mag, depth)
    slip_fac = get_slip_factor(slip)
    # Debug print showing base radius without fault-distance attenuation
    print(f"[DEBUG] R0 (depth-only)={R0:.2f}km, slip_fac={slip_fac}, avg_slip={avg_slip}, soil_factor={sw}, domsoi_factor={df}")
    fac = slip_fac * avg_slip * df
    return sw * fac * R0, sm * fac * R0, sb * fac * R0

def calculate_radii(mag, depth, fdist, slip, avg_slip, sw, sm, sb, df):
    R0 = base_radius(mag, depth, fdist)
    slip_fac = get_slip_factor(slip)
    # Debug print
    fac = slip_fac * avg_slip * df
    return sw*fac*R0, sm*fac*R0, sb*fac*R0

# --- 6) Main ---
def main():
    mag   = float(input("Magnitude: "))
    depth = float(input("Depth (km): "))
    lat   = float(input("Latitude: "))
    lon   = float(input("Longitude: "))
    sw, sm, sb, soil_code, sf = get_soil_amplification(lat, lon)
    dist, slip, avg_slip = get_fault_info(lat, lon)
    if dist is None:
        print("No fault found."); return
    print(f"Fault: {slip}, dist={dist:.2f}km, avg_slip={avg_slip}")
    print(f"Soil: {soil_code}, soil_factor={sf}")
    w,m,b = calculate_radii(mag, depth, dist, slip, avg_slip, sw, sm, sb, sf)
    print("Destruction Radii (km):")
    print(f" • Worst: {w:.2f}\n • Med  : {m:.2f}\n • Best : {b:.2f}")

if __name__=='__main__': main()
