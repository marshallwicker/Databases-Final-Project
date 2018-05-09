
var searchDictionary = {"cname":"Company Name", "ceo":"CEO Name", "state":"State", "ticker":"Ticker ID"};

function changeSearchAspect() {
    var searchKey = document.getElementById("searchon").value;
    document.getElementById("searchInput").placeholder = "Search by " + searchDictionary[searchKey];
}