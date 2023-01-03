import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, filter } from 'rxjs/operators';

@Injectable()
export class AuthenticationInterceptor implements HttpInterceptor {

  constructor() { }

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    if (localStorage.getItem('idToken')) {
      var idToken = localStorage.getItem('idToken');
    }
    else {
      var idToken = ''
    }
    return next.handle(request.clone({
      setHeaders: {
        Authorization: `Bearer ${idToken}`
      }
    }));
  }
}
