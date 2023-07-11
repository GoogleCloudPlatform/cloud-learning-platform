import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SignInComponent } from './sign-in.component';
import { E2eSignInComponent } from './e2e-sign-in/e2e-sign-in.component';

const routes: Routes = [
    {
        path: '',
        component: SignInComponent,
    },
    {
        path: 'e2e',
        component: E2eSignInComponent,
    },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class LoginRoutingModule { }