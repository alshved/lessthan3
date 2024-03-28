function send() {

    let time_inf = document.getElementById("time").value;
    let who_inf = document.getElementById("who").value;
    let cabinet_inf = document.getElementById("cabinet").value;
    $("#exampleModal").modal("hide");
    console.log("hidden");
    document.getElementById("teacher1").textContent = who_inf;
    console.log("who_inf");
    const response = fetch("/test", {
        method: "PUT",
        body: JSON.stringify({
            cabinet: cabinet_inf,
            time: time_inf,
            teacher: who_inf
        })
    })
}
fetch("/static", {method: "GET"});
console.log("SSSs");
const submit_btn = document.getElementById("submit-btn");
submit_btn.addEventListener("click", send);