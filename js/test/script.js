const { organisms, organs, celltypes } = require('..')

let result;
(async () => {

    // test organisms
    result = await organisms();
    console.log(result);

    // test organs
    result = await organs(organism = "m_musculus");
    console.log(result);

    // cell types

})();
