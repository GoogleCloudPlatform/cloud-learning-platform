import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { retry, catchError } from 'rxjs/operators';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { AuthService } from '../shared/service/auth.service';


@Injectable()
export class ErrorInterceptor implements HttpInterceptor {

  constructor(private _snackBar: MatSnackBar, private authService: AuthService) { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(catchError((error: HttpErrorResponse) => {
      let errorMsg = '';
      if (error.error instanceof ErrorEvent) {
        console.log('This is client side error');
        errorMsg = `Error: ${error.error.message}`;
      } else {
        console.log('This is server side error');
        errorMsg = `Error Code: ${error.status},  Message: ${error.message}`;
        if (error.status == 401) {
          this.authService.signOut()
        }
        else {
          // this.openFailureSnackBar('Internal Server Error', 'Close')
          console.log("error")
        }
      }
      console.log(errorMsg);
      return throwError(errorMsg);
    }));
  }


  openFailureSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 6000,
      panelClass: ['red-snackbar'],
    });
  }
}
