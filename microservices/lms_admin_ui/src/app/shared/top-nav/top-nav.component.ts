import { Component, OnInit } from '@angular/core';
import { AuthService } from '../service/auth.service';


@Component({
  selector: 'app-top-nav',
  templateUrl: './top-nav.component.html',
  styleUrls: ['./top-nav.component.scss']
})
export class TopNavComponent implements OnInit {
  userShowName: string = 'John Doe'
  constructor(private _AuthService: AuthService) { }

  ngOnInit(): void {
  }
  logout() {
    if (localStorage.getItem('idToken')) {
      localStorage.removeItem('idToken')
    }
    this._AuthService.signOut()
  }
}
