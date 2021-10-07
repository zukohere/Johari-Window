v="v2"
console.log(v)
function addData() {
    johariAdj1 = ["Able",
        "Accepting",
        "Adaptable",
        "Bold",
        "Brave",
        "Calm",
        "Caring",
        "Cheerful",
        "Clever",
        "Complex",
        "Confident",
        "Dependable",
        "Dignified",
        "Empathetic",
        "Energetic",
        "Extroverted",
        "Friendly",
        "Giving",
        "Happy",
        "Helpful"]
    johariAdj2 = ["Idealistic",
        "Independent",
        "Ingenious",
        "Intelligent",
        "Introverted",
        "Kind",
        "Knowledgeable",
        "Logical",
        "Loving",
        "Mature",
        "Modest",
        "Nervous",
        "Observant",
        "Organized",
        "Patient",
        "Powerful",
        "Proud",
        "Quiet",
        "Reflective",
        "Relaxed"]
    johariAdj3 = [
        "Religious",
        "Responsive",
        "Searching",
        "Self - assertive",
        "Self - conscious",
        "Sensible",
        "Sentimental",
        "Shy",
        "Silly",
        "Spontaneous",
        "Sympathetic",
        "Tense",
        "Trustworthy",
        "Warm",
        "Wise",
        "Witty"]
    d3.select("#DataArea0").html("Enter name, select role, and select all adjectives that apply.<br>")
    d3.select("#DataArea1").html("")
    d3.select("#DataArea2").html("")
    d3.select("#DataArea3").html("")


    var myDiv = document.getElementById("DataArea0");
    //Allow name entry.
    var namebox = document.createElement('input')
    namebox.type = "text"
    namebox.name = "JohariAdj"
    namebox.id = "id_name"
    myDiv.appendChild(namebox)

    // creating label for name entry
    var label = document.createElement('label');
    label.htmlFor = "id_name";
    label.appendChild(document.createTextNode("Enter Name."))
    myDiv.appendChild(label)
    d3.select("#DataArea0").append("br")
    //Allow selection of who it's for. ((Need Dropdown of users from mongo unless new person))

    //Allow role selection.
    roleOptions = ["Observer","Subject"]
    var roleSelect = document.createElement('select');
    roleSelect.id = "id_role"
    roleSelect.name = "JohariAdj"
    roleOptions.forEach(role => {
        var option = document.createElement("option")
        option.text = role
        option.value = role
        roleSelect.add(option)
    })
        
    myDiv.appendChild(roleSelect)
    var label = document.createElement('label');
    label.htmlFor = "id_role";
    label.appendChild(document.createTextNode("Select Role."))
    myDiv.appendChild(label)

    // appending the created text to
    // the created label tag

    var myDiv = document.getElementById("DataArea1");
    johariAdj1.forEach(element => {
        // creating checkbox element
        var checkbox = document.createElement('input');

        // Assigning the attributes
        // to created checkbox
        checkbox.type = "checkbox";
        checkbox.name = "JohariAdj";
        checkbox.value = element;
        checkbox.id = "id";

        // creating label for checkbox
        var label = document.createElement('label');

        // assigning attributes for
        // the created label tag
        label.htmlFor = "id";
        label.appendChild(document.createTextNode(element))

        // appending the checkbox
        // and label to div
        myDiv.appendChild(checkbox);
        myDiv.appendChild(label);
        d3.select("#DataArea1").append("br")
    });

    var myDiv = document.getElementById("DataArea2");

    // appending the created text to
    // the created label tag
    johariAdj2.forEach(element => {
        // creating checkbox element
        var checkbox = document.createElement('input');

        // Assigning the attributes
        // to created checkbox
        checkbox.type = "checkbox";
        checkbox.name = "JohariAdj";
        checkbox.value = element;
        checkbox.id = "id";

        // creating label for checkbox
        var label = document.createElement('label');

        // assigning attributes for
        // the created label tag
        label.htmlFor = "id";
        label.appendChild(document.createTextNode(element))

        // appending the checkbox
        // and label to div
        myDiv.appendChild(checkbox);
        myDiv.appendChild(label);
        d3.select("#DataArea2").append("br")
    });

    var myDiv = document.getElementById("DataArea3");

    // appending the created text to
    // the created label tag
    johariAdj3.forEach(element => {
        // creating checkbox element
        var checkbox = document.createElement('input');

        // Assigning the attributes
        // to created checkbox
        checkbox.type = "checkbox";
        checkbox.name = "JohariAdj";
        checkbox.value = element;
        checkbox.id = "id";

        // creating label for checkbox
        var label = document.createElement('label');

        // assigning attributes for
        // the created label tag
        label.htmlFor = "id";
        label.appendChild(document.createTextNode(element))

        // appending the checkbox
        // and label to div
        myDiv.appendChild(checkbox);
        myDiv.appendChild(label);
        d3.select("#DataArea3").append("br")
    })
    var x = document.createElement("INPUT");
    x.setAttribute("type", "submit");
    myDiv.appendChild(x)
        ;
}
addData()