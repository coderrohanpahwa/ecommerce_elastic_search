function handleAutocomplete(){
    document.getElementById("autocomplete_category").innerHTML=""
    document.getElementById("autocomplete_product").innerHTML=""
    handleAutocomplete_product();
var text = document.getElementById("Search_bar").value;
if (!text){
//    console.log("You have not written in search box")
    return
}
const query={
  "query":{
    "prefix":{
      "category.keyword": text
    }
  }
}
axios.get('http://127.0.0.1:9200/ecommerce_category_using_python/_search',{params:{source:JSON.stringify(query),source_content_type:"application/json"}}).then((res)=>{
    console.log(res['data']['hits']['total']['value']);
    if (res['data']['hits']['total']['value']==0){
//        console.log("No Result Found for entered input ");
        console.log("Capitalize the first word");
        text=text.charAt(0).toUpperCase()+text.slice(1);

        const query={
        "query":{
        "prefix":{
        "category.keyword":text
        }}}
    axios.get('http://127.0.0.1:9200/ecommerce_category_using_python/_search',{params:{source:JSON.stringify(query),source_content_type:"application/json"}}).then((inner_res)=>{

        if (inner_res['data']['hits']['total']['value']==0){
            const fuzzy_query={
                "query":{
                "match":{
                "category":{
                "query":text,
                "fuzziness":"auto"
                }
                }},
                "sort": [
     {
       "_score": {
         "order": "desc"
       }
     }
   ]
            }
    axios.get('http://127.0.0.1:9200/ecommerce_category_using_python/_search',{params:{source:JSON.stringify(fuzzy_query),source_content_type:"application/json"}}).then((response)=>{
        if (response['data']['hits']['total']['value']==0){
//            console.log("No Result found through fuzzy query");
        }
        else {
        console.log("------->",response['data']['hits']['hits']);
        var res_length=response['data']['hits']['hits'].length
        document.getElementById("autocomplete_elements").innerHTML=""
        for (var i=0;i<res_length;i++){
//            console.log("Invokded");
            document.getElementById("autocomplete_elements").innerHTML +=`<option>${response['data']['hits']['hits'][i]['_source']['category']}</option>`
        }
}
    })
        }
        else{

//            console.log(inner_res['data']['hits']['hits'][1])
            var res_length=inner_res['data']['hits']['hits'].length;

            for (var i=0;i<res_length;i++){
//                console.log("--->",inner_res['data']['hits']['hits'][i]['_source']['category'])
        }
        console.log(document.getElementById("autocomplete_category"));
            for(var i=0;i<res_length;i++){
    document.getElementById("autocomplete_category").innerHTML+=`<option>${inner_res['data']['hits']['hits'][i]['_source']['category']}</option>`
    }
            }
    })
    }
    else {
        console.log(res['data']['hits']['total']['value']);
        var res_length=res['data']['hits']['hits'].length;
        for (var i=0;i<res_length;i++){
        console.log(res['data']['hits']['hits'][i]['_source']['category']);
        document.getElementById("autocomplete_category").innerHTML+=`<option>${res['data']['hits']['hits'][i]['_source']['category']}</option>`

        }

    }

})
}