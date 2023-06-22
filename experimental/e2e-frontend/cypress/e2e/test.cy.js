/// <reference types="cypress" />

context('Window', () => {
    it('cy.window() - get the global window object', () => {
        let mainUrl = null
        let token = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjY3YmFiYWFiYTEwNWFkZDZiM2ZiYjlmZjNmZjVmZTNkY2E0Y2VkYTEiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiUmFtIENoYXVkaGFyaSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BRWRGVHA0d0l4Um53NTBoVzdfYmppcVlPTWdkaHB0MEd6OWR3MUQ2THBPQT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9jb3JlLWxlYXJuaW5nLXNlcnZpY2VzLWRldiIsImF1ZCI6ImNvcmUtbGVhcm5pbmctc2VydmljZXMtZGV2IiwiYXV0aF90aW1lIjoxNjg3MTczNTIxLCJ1c2VyX2lkIjoiTkh2cEJBZTVFTFJ4aVZJWDdDR0VsUHRwck5qMiIsInN1YiI6Ik5IdnBCQWU1RUxSeGlWSVg3Q0dFbFB0cHJOajIiLCJpYXQiOjE2ODcxNzM1MjEsImV4cCI6MTY4NzE3NzEyMSwiZW1haWwiOiJyYW0uY2hhdWRoYXJpQHF1YW50aXBoaS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExNTExMzc3MTk1MzUxNTAyMTQyMiJdLCJlbWFpbCI6WyJyYW0uY2hhdWRoYXJpQHF1YW50aXBoaS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.EnJHE2uH9qF1iGhG3Q8Fl54RU_XK4T-D2WZniMYTzeCFTTV3AcEDvC6boaQ5lC2Kj22NEjBY4Wm0I4YcpUbyobpYDvawmhnY4MmUGUNEzIo0iGaegvqdJLw1YFAcaWH5k0AhNCwx80hpBjha7aqNhJ-YBnK6dLB5Dhreh7cO7IS5rnl5O_KIuK3nt-p7TQk4dCzYxL-n1-kNrufzloWc6e1F0q_dbm3Ve579gK_qIS_-Bed0DsN_69QwSaJ0FB4uIaCyhVQlAS8S6LGVyipwlARg1hfHQGvnqbktY-_X2auIWXoihZkwsWIhG9JVm2RjuEoMB3_r4pI3xAV0eQYWvA"
        cy.request({
            url: 'https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/content-selection-launch-init?tool_id=xwsBdJzPESMQWiQw7Plh&user_id=vcmt4ZemmyFm59rDzl1U&context_id=n5XppUsogIgTq7iQTKE5&context_type=section',
            method: "GET",
            headers: {
                Authorization: token
            }
        }).then((response) => {
            expect(response.body).to.have.property('url')
            mainUrl = response.body.url
            cy.request({
                url: mainUrl,
                method: "GET",
                followRedirect: true
            }).then((response) => {
                console.log("main response", response)
                expect(response.status).to.equal(200)
            })
        })
    })

})