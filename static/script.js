let chart; // global chart variable

async function analyze() {

    const username = document.getElementById("username").value;
    document.getElementById("result").innerHTML = "Loading...";

    const response = await fetch(`/api/${username}`);
    const data = await response.json();
    if (data.error) {
    document.getElementById("result").innerHTML = "User not found.";
    return;
}
    const user = data.user;

    let repoList = "";

    data.top_repos.forEach(repo => {
        repoList += `
        <li>
            <a href="${repo.html_url}" target="_blank">
                ${repo.name}
            </a> ⭐ ${repo.stargazers_count}
        </li>`;
    });

    document.getElementById("result").innerHTML = `
        <h2>${user.login}</h2>
        <img src="${user.avatar_url}" width="100">

        <p><b>Followers:</b> ${user.followers}</p>
        <p><b>Public Repos:</b> ${user.public_repos}</p>

        <hr>

        <p><b>Total Stars:</b> ${data.total_stars}</p>
        <p><b>Most Used Language:</b> ${data.most_used_language}</p>

        <h3>Top 5 Repositories</h3>
        <ul>
            ${repoList}
        </ul>
    `;

    const languages = data.languages;

    const labels = Object.keys(languages);
    const values = Object.values(languages);

    const ctx = document.getElementById("languageChart").getContext("2d");

    // destroy old chart if exists
    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                data: values
            }]
        }
    });

}