import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { SharedModule } from './shared/shared.module';
import { MaterialSharedModule } from './shared/material-shared.module';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
// import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    RouterModule,
    SharedModule,
    MaterialSharedModule,
    HttpClientModule,
  ],
  // providers: [
  //   { provide: MatDialogRef, useValue: {} },

  //   { provide: MAT_DIALOG_DATA, useValue: {} }
  // ],
  bootstrap: [AppComponent]
})
export class AppModule { }
