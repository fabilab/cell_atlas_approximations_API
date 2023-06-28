const atlasapprox = require('..')

let result;
(async () => {

    // test organisms
    result = await atlasapprox.organisms();
    console.log(result);

    // test organs
    result = await atlasapprox.organs(organism = "m_musculus");
    console.log(result);

    // cell types
    result = await atlasapprox.celltypes(organism = "m_musculus", organ = "Lung");
    console.log(result);

    // average
    result = await atlasapprox.average(organism = "m_musculus", organ = "Lung", features=["Col1a1", "Ptprc"]);
    console.log(result);

    // fraction expressing
    result = await atlasapprox.fraction_detected(organism = "m_musculus", organ = "Lung", features=["Col1a1", "Ptprc"]);
    console.log(result);

    // markers
    result = await atlasapprox.fraction_detected(organism = "m_musculus", organ = "Lung", celltype="fibroblast");
    console.log(result);

    // highest measurement
    result = await atlasapprox.highest_measurement(organism = "m_musculus", feature = "Ins1");
    console.log(result);

    // similar features
    result = await atlasapprox.similar_features(organism = "m_musculus", organ = "Lung", feature = "Ins1");
    console.log(result);

    // similar cell types
    result = await atlasapprox.similar_celltypes(organism = "m_musculus", organ = "Lung", celltype = "fibroblast", features=["Col1a1", "Col1a2"]);
    console.log(result);
    
    // cell type x organ table
    result = await atlasapprox.celltypexorgan(organism = "m_musculus");
    console.log(result);
    
    // data sources
    result = await atlasapprox.data_sources();
    console.log(result);

})();
