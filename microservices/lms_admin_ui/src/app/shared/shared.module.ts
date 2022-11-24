import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TopNavComponent } from './top-nav/top-nav.component';
import { MaterialSharedModule } from './material-shared.module';


@NgModule({
  declarations: [

    TopNavComponent
  ],
  imports: [
    CommonModule,
    MaterialSharedModule
  ],
  exports: [
    TopNavComponent
  ]
})
export class SharedModule { }
