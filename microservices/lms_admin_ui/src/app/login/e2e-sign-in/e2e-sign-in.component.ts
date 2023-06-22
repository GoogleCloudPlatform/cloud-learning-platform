import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../shared/service/auth.service';
import { MatIconRegistry } from "@angular/material/icon";
import { DomSanitizer } from "@angular/platform-browser";
import { environment } from 'src/environments/environment';
import { FormControl, UntypedFormGroup, UntypedFormBuilder, Validators, Form } from '@angular/forms';

@Component({
  selector: 'app-e2e-sign-in',
  templateUrl: './e2e-sign-in.component.html',
  styleUrls: ['./e2e-sign-in.component.scss']
})
export class E2eSignInComponent implements OnInit{
  loginForm: UntypedFormGroup
  constructor(public authService: AuthService, private matIconRegistry: MatIconRegistry, 
    private domSanitizer: DomSanitizer,private fb: UntypedFormBuilder,) {
    console.log('env var', environment.apiurl);
    console.log('firebase var', environment.firebase.projectId);
    console.log('firebase var', environment.firebase.apiKey);
    console.log('firebase var', environment.firebase.appId);
    this.matIconRegistry.addSvgIcon(
      'google-icon',
      this.domSanitizer.bypassSecurityTrustResourceUrl('assets/img/Google.svg')
    );
    this.matIconRegistry.addSvgIcon(
      'google-text-icon',
      this.domSanitizer.bypassSecurityTrustResourceUrl('assets/img/google-text.svg')
    );
  }
  ngOnInit(): void {
    this.loginForm = this.fb.group({
      email: this.fb.control('', [Validators.required,Validators.email]),
      password: this.fb.control('', [Validators.required]),
    });
  }

  login(){
console.log(this.loginForm.value)
this.authService.emaiAndPasswordSignIn(this.loginForm.value['email'],this.loginForm.value['password'])
  }
}
