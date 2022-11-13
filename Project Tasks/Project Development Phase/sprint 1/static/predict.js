$(()=>{

    const getData = () => {
        const jsonData = {};
        jsonData.price = "hi";
        return JSON.stringify(jsonData);
    };

    const postResult = (result) => $("#result").val(result);

    $("#submit").on("click",()=>{
        jQuery.ajax({
            url :"/predict",
            contentType : "application/json; charset=utf-8",
            data : getData(),
            type : "POST",
            success : (result)=> postResult(result),
            failure : (result) => postResult(result) 
        });
    });
});