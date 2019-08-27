$_1('head').append('<link rel="stylesheet" type="text/css" href="///code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">');
$_1('head').append('<link rel="stylesheet" type="text/css" href="flightairline//resources/demos/style.css">');
$_1(function () {
    var airports = ["aa"];
    $_1("#flight_from").autocomplete({
        source: function (request, response) {
            $.get("/airport/api", {q: request.term}, function (data) {
                response(data);
            });
        },
    });
    $_1("#flight_to").autocomplete({
        source: function (request, response) {
            $.get("/airport/api", {q: request.term}, function (data) {
                response(data);
            });
        },
    });
    $_1(function () {
        $_1.datepicker.setDefaults($_1.datepicker.regional["de"]);
        $_1("#departure_date").datepicker();
        $_1("#return_flight_date").datepicker();
    });
});
$_1(document).ready(function () {
    document.getElementById("flight_from").focus();
    document.getElementById("submit_request").onclick = function (e) {
        this.disabled = true;
        this.style.opacity = "0.5";
        let original_button_text = this.innerText;
        this.innerText = "In Bearbeitung ... ";
        let flight_from = document.getElementById("flight_from").value;
        let flight_to = document.getElementById("flight_to").value;
        let amount_adults = document.getElementById("adults").options[document.getElementById("adults").selectedIndex].value;
        let amount_children = document.getElementById("children").options[document.getElementById("children").selectedIndex].value;
        let departure_date = document.getElementById("departure_date").value;
        let return_flight_date = document.getElementById("return_flight_date").value;
        let travel_class = document.getElementById("travel_class").options[document.getElementById("travel_class").selectedIndex].value;
        let flight_type_selection = $_1('input[name="flight-type"]:checked');
        let flight_type = "";
        if (flight_type_selection.length > 0) {
            flight_type = flight_type_selection.val();
        }
        let phone = document.getElementById("phone").value;

        let submit_request_btn = this;

        $.ajax({
            method: "POST",
            url: "{% url 'request:mail' %}",
            data: {
                flight_from: flight_from, flight_to: flight_to, amount_adults: amount_adults,
                amount_children: amount_children, departure_date: departure_date,
                return_flight_date: return_flight_date, "csrfmiddlewaretoken": "{{ csrf_token }}",
                travel_class: travel_class, flight_type: flight_type, phone: phone
            }
        })
            .done(function (data) {
                let success_box = document.getElementById("success_box");
                success_box.style.display = "";
                submit_request_btn.removeAttribute("disabled");
                submit_request_btn.style.opacity = "";
                submit_request_btn.innerText = original_button_text;
                document.getElementById("main_form").reset();

            }).fail(function (data) {
            function findAncestor(el, cls) {
                while ((el = el.parentNode) && el.className.indexOf(cls) < 0) ;
                return el;
            }

            submit_request_btn.removeAttribute("disabled");
            submit_request_btn.style.opacity = "";
            submit_request_btn.innerText = original_button_text;
            let responseJSON = data.responseJSON;
            if (responseJSON.message == "form_error") {
                let errors = responseJSON.errors;
                for (let i = 0; i < Object.keys(errors).length; i++) {
                    let input_field = Object.keys(errors)[i];
                    let error_messages = errors[input_field];
                    let error_input = document.getElementById(input_field);
                    if (error_input) {
                        let error_field = document.getElementById(input_field + "_error");
                        error_field.innerText = error_messages;
                        let form_group = findAncestor(error_field, "form-group");
                        if (!toString(form_group.className).includes("has-error")) {
                            form_group.className += " has-error";
                        }
                    }
                }
            }
        });

    };
});
