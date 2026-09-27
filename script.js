const form = document.getElementById("cropForm");

const cropName = document.getElementById("cropName");

const result = document.getElementById("result");

const magicLoader = document.getElementById("magicLoader");


form.addEventListener("submit", async function (event) {

    event.preventDefault();


    /* ========================= */
    /* GET USER INPUT */
    /* ========================= */

    const data = {

        N: parseFloat(
            document.getElementById("nitrogen").value
        ),

        P: parseFloat(
            document.getElementById("phosphorus").value
        ),

        K: parseFloat(
            document.getElementById("potassium").value
        ),

        temperature: parseFloat(
            document.getElementById("temperature").value
        ),

        humidity: parseFloat(
            document.getElementById("humidity").value
        ),

        ph: parseFloat(
            document.getElementById("ph").value
        ),

        rainfall: parseFloat(
            document.getElementById("rainfall").value
        )

    };


    /* ========================= */
    /* HIDE OLD RESULT */
    /* ========================= */

    result.style.display = "none";

    result.classList.remove("show-result");


    /* ========================= */
    /* SHOW MAGIC */
    /* ========================= */

    magicLoader.classList.add("active");


    /* ========================= */
    /* DISABLE BUTTON */
    /* ========================= */

    const button =
        form.querySelector("button");


    button.disabled = true;

    button.textContent =
        "✨ Analyzing...";


    try {


        /* ========================= */
        /* SEND DATA TO PYTHON */
        /* ========================= */

        const response = await fetch(
            "/predict",
            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body:
                    JSON.stringify(data)

            }
        );


        /* ========================= */
        /* GET PREDICTION */
        /* ========================= */

        const prediction =
            await response.json();


        /* ========================= */
        /* MAGIC DELAY */
        /* ========================= */

        await new Promise(
            function (resolve) {

                setTimeout(
                    resolve,
                    1800
                );

            }
        );


        /* ========================= */
        /* HIDE MAGIC */
        /* ========================= */

        magicLoader.classList.remove(
            "active"
        );


        /* ========================= */
        /* SHOW RESULT */
        /* ========================= */

        cropName.textContent =
            prediction.crop;


        result.style.display =
            "block";


        result.classList.add(
            "show-result"
        );


    }


    catch (error) {


        console.error(error);


        magicLoader.classList.remove(
            "active"
        );


        result.style.display =
            "block";


        cropName.textContent =
            "Something went wrong";


        result.classList.add(
            "show-result"
        );

    }


    /* ========================= */
    /* ENABLE BUTTON */
    /* ========================= */

    button.disabled = false;

    button.textContent =
        "🌾 Recommend Crop";


});