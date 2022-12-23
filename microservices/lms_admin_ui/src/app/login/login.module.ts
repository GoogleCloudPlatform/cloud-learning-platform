import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SignInComponent } from './sign-in.component';
import { LoginRoutingModule } from './login.routing.module';
import { SharedModule } from '../shared/shared.module';
import { MaterialSharedModule } from '../shared/material-shared.module';


@NgModule({
  declarations: [
    SignInComponent,
  ],
  imports: [
    CommonModule,
    LoginRoutingModule,
    SharedModule,
    MaterialSharedModule,
  ]
})
export class LoginModule { }
