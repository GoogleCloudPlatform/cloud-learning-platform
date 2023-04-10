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
      let errorObj = {}
      if (error.error instanceof ErrorEvent) {
        console.log('This is client side error');
        errorMsg = `Error: ${error.error.message}`;
      } else {
        if (error.status == 401) {
          this.authService.signOut()
        }
        else {
          this.openFailureSnackBar(error.error.message?'Error : '+error.error.message:'Error : Internal Server Error', 'Close')
        }
        errorObj['status'] = error.status
        errorObj['message'] = error.error.message
      }
      return throwError(errorObj);
    }));
  }


  openFailureSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 6000,
      panelClass: ['red-snackbar'],
    });
  }
}
