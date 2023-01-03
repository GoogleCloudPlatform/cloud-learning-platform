
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import * as auth from 'firebase/auth';
import { AngularFireAuth } from '@angular/fire/compat/auth';
import {
  AngularFirestore,
  AngularFirestoreDocument,
} from '@angular/fire/compat/firestore';
import { Router } from '@angular/router'

import { Observable, of } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  userData: any
  user$: Observable<any>
  constructor(
    private afAuth: AngularFireAuth,
    private afs: AngularFirestore,
    private router: Router,
    private http: HttpClient,
    private _snackBar: MatSnackBar,
  ) {

    this.user$ = this.afAuth.authState.pipe(
      switchMap(user => {
        // Logged in
        if (user) {
          console.log('user', user)
          user.getIdToken().then(idToken => {
            console.log('id token', idToken)
            localStorage.setItem('idToken', idToken)
            if (idToken) {
              this.router.navigate(['/home'])
            }
          });
          return this.afs.doc<any>(`users/${user.uid}`).valueChanges();
        } else {
          // Logged out
          return of(null);
        }
      })
    )

  }


  async googleSignin() {
    const provider = new auth.GoogleAuthProvider();
    const credential = await this.afAuth.signInWithPopup(provider);
    console.log('user', credential.user.displayName)
    localStorage.setItem('user', credential.user.displayName)
    credential.user?.getIdToken().then(idToken => {
      localStorage.setItem('idToken', idToken)
      this.validate().subscribe((res: any) => {
        // console.log(res)
        if (res.success == true) {
          if (idToken) {
            this.router.navigate(['/home'])
          }
        }
        else {
          this.openFailureSnackBar('Authentication Failed', 'Close')
        }
      }, (error: any) => {
        this.openFailureSnackBar('Authentication Failed', 'Close')
      })

    });
  }

  private updateUserData(user: any) {
    // Sets user data to firestore on login
    const userRef: AngularFirestoreDocument<any> = this.afs.doc(`users/${user.uid}`);

    const data = {
      uid: user.uid,
      email: user.email,
      displayName: user.displayName,
      photoURL: user.photoURL
    }

    return userRef.set(data, { merge: true })

  }

  async signOut() {
    await this.afAuth.signOut();
    this.router.navigate(['/login']);
  }

  validate() {
    return this.http.get(`${environment.auth_apiUrl}validate`)
  }
  openFailureSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 6000,
      panelClass: ['red-snackbar'],
    });
  }

}
