function checkPasswordStrength(password) {
    let validations = [
        password.search(/[A-Z]/) > -1,
        password.search(/[a-z]/) > -1,
        password.search(/\d/) > -1,
        password.length > 8,
    ];

    return validations.reduce((acc, curr) => curr + acc) >= 4;
}

class User {
    constructor(nameOrObj, id, creation, lastLogin) {
        if (nameOrObj instanceof String) {
            this.name = name;
            this.id = id;
            this.creation = creation;
            this.lastLogin = lastLogin;
        } else if (nameOrObj instanceof Object) {
            this.name = nameOrObj.name;
            this.id = nameOrObj.id;
            this.creation = nameOrObj.creation;
            this.lastLogin = nameOrObj.last_login;
            this.loginId = nameOrObj.login_id | null;
        }
    }

    // Instantiate a new User with data from the server
    static async getFromServer(id) {
        if (!isNaN(id)) {
            throw new TypeError("Argument id has to be a string");
        }

        return fetch(`http://127.0.0.1:5000/user/${id}`, {
            mode: "no-cors",
        })
            .then(data => data.json())
            .then(json => new User(json));
    }

    // Get a list of multiple user accounts at once
    static async getMultiple(perPage, page, orderBy, descending) {
        let argumentsGiven =
            [perPage, page, orderBy, descending].filter(e => e != undefined)
                .length >= 1;
        let url = `http://127.0.0.1:5000/user${argumentsGiven ? "?" : ""}`;

        if (perPage != undefined) {
            url += `per_page=${perPage}&`;
        }

        if (page != undefined) {
            url += `page=${page}&`;
        }

        if (orderBy != undefined) {
            url += `order_by=${orderBy}&`;
        }

        if (descending != undefined) {
            url += `descending=${descending}`;
        }

        if (argumentsGiven) {
            url = url.slice(0, -1);
        }

        return fetch(url, {
            mode: "no-cors",
        })
            .then(data => data.json())
            .then(json => json.map(obj => new User(obj)));
    }

    static async create(name, password) {
        password = password.toString();

        if (!checkPasswordStrength(password)) {
            console.warn(
                "The provided password does not meet common security requirements!"
            );
        }

        return fetch("http://127.0.0.1:5000/user", {
            method: "POST",
            mode: "no-cors",
            headers: new Headers({ "Content-Type": "application/json" }),
            body: JSON.stringify({
                name: name.toString(),
                password: password,
            }),
        })
            .then(console.log)
            .then(json => new User(json));
    }
}
