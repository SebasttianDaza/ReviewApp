'use strict';
{
    document.addEventListener("submit", (e) => {
        if (
            e.target.matches("#login-form") &&
            e.submitter &&
            e.submitter.defaultValue === "Log in Twitter"
        ) {
            e.preventDefault();
            let signinURL = document.querySelector("input[name='token_twitter']");
            if (signinURL) {
                window.open(
                    signinURL.getAttribute("value"),
                    "_self",
                );
            }
        }
    });
}