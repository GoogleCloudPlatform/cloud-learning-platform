import { Component } from '@angular/core';
import { Router, NavigationStart, NavigationEnd, Event as NavigationEvent } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'lms_admin_ui';
  showTopNav: boolean = true
  constructor(private router: Router,) {
    this.router.events.subscribe(
      (event: NavigationEvent) => {
        if (event instanceof NavigationEnd) {
          if (event.url == '/login') {
            this.showTopNav = false
          }
          else {
            this.showTopNav = true
          }
        }
      })
  }
}
