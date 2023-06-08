import * as firebase from "firebase/app";
import "firebase/storage";
import "firebase/auth";
import { GoogleAuthProvider, getAuth, signOut } from "firebase/auth";

const appUrl = `https://${process.env.API_DOMAIN}`;

const app = firebase.initializeApp({
	apiKey: process.env.FIREBASE_API_KEY,
	authDomain: process.env.FIREBASE_AUTH_DOMAIN,
});

export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();

export const getCurrentLoginStatus = async () => {
	if (auth.currentUser) {
		const idToken = await auth.currentUser.getIdToken(true).then(t => t)
		typeof window !== "undefined" && localStorage.setItem("idToken", idToken)
		return true
	} else {
		return false
	}
}

export const logout = (afterAction = () => { }) => {
	signOut(auth).then(r => afterAction(null));
};

export const passLoginConditions = async () => {
	const loggedEmailDomain = await auth.currentUser.email.split('@')[1]
	const idToken = await auth.currentUser.getIdToken(true).then(t => t)
	let status = {}
	let whitelistStatus = await checkWhitelistingStatus(loggedEmailDomain);
	if (whitelistStatus) {
		typeof window !== "undefined" && localStorage.setItem("idToken", idToken)
		status = { msg: "", status: true }
	}
	else {
		const isUserWhitelisted = await validateToken(idToken)
		if (isUserWhitelisted) {
			typeof window !== "undefined" && localStorage.setItem("idToken", idToken)
			status = { msg: "", status: true }
		} else {
			logout()
			status = { msg: "Access denied", status: false }
		}
	}
	return status
}

const checkWhitelistingStatus = async (loggedEmailDomain) => {
	let authorized = false;
	if (process.env.WHITELIST_DOMAINS) {
		let whitelistedDomains = (process.env.WHITELIST_DOMAINS).replace(' ', '').split(',')
		if (whitelistedDomains.includes(loggedEmailDomain)) {
			authorized = true;
		}
	}
	return authorized;
}

const validateToken = async (token) => {
	const myHeaders = new Headers();
	myHeaders.append("Accept", "application/json");
	myHeaders.append("Authorization", `Bearer ${token}`);

	var requestOptions = {
		method: "GET",
		headers: myHeaders,
	};

	const resp = await fetch(`${appUrl}/authentication/api/v1/validate`, requestOptions)
		.then(response => response.json()).then(response => {
			const data = response.data.access_api_docs ? response.data.access_api_docs : false
			return data
		})
		.catch(err => {
			console.log(err)
			return false
		})
	return resp
}
