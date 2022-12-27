import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';
import { Router } from '@angular/router';
import { take, map, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(public authService: AuthService, private router: Router) { }
  canActivate(): boolean {
    if (localStorage.getItem('idToken')) {
      return true
    }
    else {
      this.router.navigate(['/login'])
      return false
    }
  }

}
