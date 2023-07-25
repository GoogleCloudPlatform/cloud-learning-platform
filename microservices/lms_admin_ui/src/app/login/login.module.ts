import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SignInComponent } from './sign-in.component';
import { LoginRoutingModule } from './login.routing.module';
import { SharedModule } from '../shared/shared.module';
import { MaterialSharedModule } from '../shared/material-shared.module';
import { E2eSignInComponent } from './e2e-sign-in/e2e-sign-in.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    SignInComponent,
    E2eSignInComponent,
  ],
  imports: [
    CommonModule,
    LoginRoutingModule,
    SharedModule,
    MaterialSharedModule,
    FormsModule,
    ReactiveFormsModule
  ]
})
export class LoginModule { }
