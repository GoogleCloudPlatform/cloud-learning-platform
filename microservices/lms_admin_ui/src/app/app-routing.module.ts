import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './shared/service/auth.guard';

const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'home' },
  {
    path: 'login',
    loadChildren: () => import('./login/login.module').then(m => m.LoginModule),
  },
  {
    path: 'home',
    canActivate: [AuthGuard],
    loadChildren: () => import('./home/home.module').then(m => m.HomeModule),
  },
  {
    path: 'lti-tools',
    canActivate: [AuthGuard],
    loadChildren: () => import('./lti/lti.module').then(m => m.LtiModule),
  },
  {
    path: 'jobs',
    canActivate: [AuthGuard],
    loadChildren: () => import('./batch-jobs/batch-jobs.module').then(m => m.JobsModule),
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
