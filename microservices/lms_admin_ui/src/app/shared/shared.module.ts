import { NgModule } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { TopNavComponent } from './top-nav/top-nav.component';
import { MaterialSharedModule } from './material-shared.module';
import { BreadcrumComponent } from './breadcrum/breadcrum.component';
import { RouterModule } from '@angular/router';

@NgModule({
  declarations: [

    TopNavComponent,
    BreadcrumComponent
  ],
  imports: [
    CommonModule,
    MaterialSharedModule,
    RouterModule
  ],
  exports: [
    TopNavComponent,
    BreadcrumComponent
  ],
  providers: [
    DatePipe
  ]
})
export class SharedModule { }
