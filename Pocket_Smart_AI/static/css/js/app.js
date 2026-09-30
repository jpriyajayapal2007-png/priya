function money(value) {

    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0
        }
    ).format(
        Number(value || 0)
    );
}


function escapeHtml(value) {

    return String(value).replace(
        /[&<>"']/g,

        function (character) {

            const entities = {

                "&": "&amp;",

                "<": "&lt;",

                ">": "&gt;",

                '"': "&quot;",

                "'": "&#039;"
            };

            return entities[
                character
            ];
        }
    );
}


function renderResult(data) {

    const recommendations =
        (data.recommendations || [])
            .map(

                function (recommendation) {

                    return `

                    <div class="rec">

                        <strong>
                            ${escapeHtml(
                                recommendation.name ||
                                "Recommendation"
                            )}
                        </strong>

                        <span>
                            ${escapeHtml(
                                recommendation.category ||
                                ""
                            )}

                            ·

                            ${escapeHtml(
                                recommendation.platform ||
                                ""
                            )}
                        </span>

                        <div class="price">

                            ${money(
                                recommendation.estimated_price
                            )}

                        </div>

                        ${
                            recommendation.search_url &&
                            recommendation.search_url !== "#"

                            ?

                            `
                            <a
                                target="_blank"
                                rel="noopener"
                                href="${recommendation.search_url}"
                            >
                                Search platform →
                            </a>
                            `

                            :

                            ""
                        }

                        <p>

                            ${escapeHtml(
                                recommendation.why ||
                                recommendation.price_note ||
                                ""
                            )}

                        </p>

                    </div>

                    `;
                }
            )
            .join("");


    const allocation =
        (data.allocation || [])
            .map(

                function (item) {

                    return `

                    <div class="history-row">

                        <b>
                            ${escapeHtml(
                                item.category
                            )}
                        </b>

                        <span>
                            ${money(
                                item.amount
                            )}
                        </span>

                    </div>

                    `;
                }
            )
            .join("");


    const tips =
        (data.tips || [])
            .map(

                function (tip) {

                    return `

                    <li>
                        ${escapeHtml(tip)}
                    </li>

                    `;
                }
            )
            .join("");


    return `

        <section class="result card">

            <p>

                <b>
                    Mode:
                </b>

                ${escapeHtml(
                    data.source || "demo"
                )}

            </p>


            <h2>

                ${escapeHtml(
                    data.summary ||
                    "Your plan"
                )}

            </h2>


            <div class="result-grid">

                <div>

                    <h3>
                        Budget allocation
                    </h3>

                    ${allocation}

                </div>


                <div>

                    <h3>
                        Suggestions
                    </h3>

                    ${recommendations}

                </div>

            </div>


            <h3>
                Tips
            </h3>

            <ul>
                ${tips}
            </ul>

        </section>

    `;
}


async function submitJSON(
    url,
    body
) {

    const result =
        document.getElementById(
            "result"
        );


    result.innerHTML = `

        <div class="card">
            Generating...
        </div>

    `;


    try {

        const response =
            await fetch(

                url,

                {

                    method:
                        "POST",

                    headers:
                        {
                            "Content-Type":
                                "application/json"
                        },

                    body:
                        JSON.stringify(body)
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Request failed"
            );
        }


        result.innerHTML =
            renderResult(
                data
            );


    } catch (error) {

        result.innerHTML = `

            <div class="error">

                ${escapeHtml(
                    error.message
                )}

            </div>

        `;
    }
}


const homeForm =
    document.getElementById(
        "home-form"
    );


if (homeForm) {

    homeForm.addEventListener(
        "submit",

        async function (event) {

            event.preventDefault();


            const items =
                document
                    .getElementById(
                        "items"
                    )
                    .value

                    .split("\n")

                    .filter(
                        line =>
                            line.trim()
                    )

                    .map(

                        function (line) {

                            const parts =
                                line.split(",");


                            return {

                                category:
                                    parts[0].trim(),

                                quantity:
                                    Number(
                                        parts[1] ||
                                        1
                                    )
                            };
                        }
                    );


            const body = {

                budget:
                    Number(
                        document
                            .getElementById(
                                "budget"
                            )
                            .value
                    ),

                city:
                    document
                        .getElementById(
                            "city"
                        )
                        .value,

                style:
                    document
                        .getElementById(
                            "style"
                        )
                        .value,

                rooms:
                    document
                        .getElementById(
                            "rooms"
                        )
                        .value

                        .split(",")

                        .map(
                            item =>
                                item.trim()
                        )

                        .filter(
                            Boolean
                        ),

                items:
                    items
            };


            await submitJSON(
                "/generate-home",
                body
            );

        }
    );
}


const partyForm =
    document.getElementById(
        "party-form"
    );


if (partyForm) {

    partyForm.addEventListener(
        "submit",

        async function (event) {

            event.preventDefault();


            const body = {

                budget:
                    Number(
                        document
                            .getElementById(
                                "budget"
                            )
                            .value
                    ),

                guests:
                    Number(
                        document
                            .getElementById(
                                "guests"
                            )
                            .value
                    ),

                event_type:
                    document
                        .getElementById(
                            "event_type"
                        )
                        .value,

                venue:
                    document
                        .getElementById(
                            "venue"
                        )
                        .value,

                city:
                    document
                        .getElementById(
                            "city"
                        )
                        .value,

                food_preference:
                    document
                        .getElementById(
                            "food_preference"
                        )
                        .value
            };


            await submitJSON(
                "/generate-party",
                body
            );

        }
    );
}


const jewelryForm =
    document.getElementById(
        "jewelry-form"
    );


if (jewelryForm) {

    jewelryForm.addEventListener(
        "submit",

        async function (event) {

            event.preventDefault();


            const result =
                document.getElementById(
                    "result"
                );


            result.innerHTML = `

                <div class="card">
                    Generating...
                </div>

            `;


            try {

                const response =
                    await fetch(

                        "/generate-jewelry",

                        {

                            method:
                                "POST",

                            body:
                                new FormData(
                                    jewelryForm
                                )
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.detail ||
                        "Request failed"
                    );
                }


                result.innerHTML =
                    renderResult(
                        data
                    );


            } catch (error) {

                result.innerHTML = `

                    <div class="error">

                        ${escapeHtml(
                            error.message
                        )}

                    </div>

                `;
            }

        }
    );
}