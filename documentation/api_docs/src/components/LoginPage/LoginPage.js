import React from 'react';
import './login.css';


const LoginPage = props => {

	const handelTrigger = (event) => {
		event.preventDefault();
		const email = event.target.email.value
		const password = event.target.password.value
		props.submit(email, password)
	}
	const googleSignIn = (event) => {
		event.preventDefault();
		props.signInWithGoogle()
	}

	return (
		<div className="app">
			<div className="login-form">
				<div className="title">Sign In</div>
				<div className="form">
					<form onSubmit={handelTrigger}>
						<div className="input-container">
							<label>Email</label>
							<input type="email" name="email" required />
						</div>
						<div className="input-container">
							<label>Password</label>
							<input type="password" name="password" required />
						</div>
						<div className="button-container">
							<input type="submit" value="Login" />
						</div>
						<div className="or-container">
							<div className="line-separator"></div>
							<div className="or-label">or</div>
							<div className="line-separator"></div>
						</div>
						<div className="button-container">
							<button className='google-sign-in-btn' onClick={googleSignIn}>
								<div className='google-logo'>
									<svg width="18px" height="18px" viewBox="0 0 48 48"><g>
										<path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path>
										<path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path>
										<path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"></path>
										<path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path>
										<path fill="none" d="M0 0h48v48H0z"></path></g>
									</svg>
								</div>
								<div className='google-sign-in-text'>
									Sign In with Google
								</div>
							</button>
						</div>
						{
							props.errorMessage
							&&
							<div className="error">{props.errorMessage}</div>
						}
					</form>
				</div>
			</div>
		</div>
	);
};

export default LoginPage;