CREATE DATABASE my_datbase;
CREATE TABLE data (
    id SERIAL PRIMARY KEY,
    Longitude DOUBLE PRECISION,
    Latitude DOUBLE PRECISION,
    Sigma0_VV DOUBLE PRECISION,
    Sigma0_VH DOUBLE PRECISION,
    Hrms DOUBLE PRECISION,
    Dielectric_constant DOUBLE PRECISION,
    Soil_moisture DOUBLE PRECISION,
    SM_norm DOUBLE PRECISION,
    dpsvi DOUBLE PRECISION,
    vh_veg DOUBLE PRECISION,
    L_value DOUBLE PRECISION,
    veg DOUBLE PRECISION,
    soil DOUBLE PRECISION,
    l_wcm DOUBLE PRECISION,
    veg_wcm DOUBLE PRECISION,
    soil_wcm DOUBLE PRECISION,
    hrms_soil DOUBLE PRECISION,
    Realpart_Dielectric DOUBLE PRECISION,
    DE_real_norm DOUBLE PRECISION,
    CC DOUBLE PRECISION
);

copy data (Longitude,Latitude,Sigma0_VV,Sigma0_VH,Hrms,Dielectric_constant,Soil_moisture,SM_norm,dpsvi,vh_veg,L_value,veg,soil,l_wcm,veg_wcm,soil_wcm,hrms_soil,Realpart_Dielectric,DE_real_norm,CC)
FROM 'D:\PA_CTF\All_param.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM data;
