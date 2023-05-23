import { Component, ViewChild, Inject,HostListener } from '@angular/core';
import { LtiService } from '../service/lti.service';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { DomSanitizer } from '@angular/platform-browser';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';

@Component({
  selector: 'app-content-selector',
  templateUrl: './content-selector.component.html',
  styleUrls: ['./content-selector.component.scss']
})
export class ContentSelectorComponent {
  loadingIframe = true
  iframeUrl: any = null
  isContentItemId:boolean=true
  constructor(
    private _snackBar: MatSnackBar,
    private sanitizer: DomSanitizer,
    public dialogRef: MatDialogRef<ContentSelectorComponent>,
    @Inject(MAT_DIALOG_DATA) public dialogData: any, public ltiService: LtiService
  ) {
    console.log(dialogData)
    this.getToolUrl()
    // window.addEventListener('message', e => {
    //   // Get the sent data
    //   console.log("coded", e)
    //   // const data = e.data;
    //   // const decoded = JSON.parse(data);
    //   // console.log("decoded", decoded)
    //   // this.dialogRef.close({ data: 'abc' });
    // });
    // localStorage.setItem("contentItemId",'ZOFyk4JiRJtqdsW29erH')
    if(localStorage.getItem("contentItemId")){
      localStorage.removeItem('contentItemId')
    }

  }
  getToolUrl() {
    let data = this.dialogData.extra_data
    this.ltiService.contentSelectionLaunch(data.toolId, data.userId, data.contextId, data.contextType).subscribe(
      (response: any) => {
        this.loadingIframe = false
        this.iframeUrl = response.url
        this.isContentItemId=false        
      }
    )
  }
  get_content_item_id(){
    if(localStorage.getItem('contentItemId')){
      this.openSuccessSnackBar('content item id copied to create assignment form','Success')
      this.dialogRef.close({ data: localStorage.getItem('contentItemId') });
    }
    else{
      this.openFailureSnackBar('content item if not available', 'Error')
    }
  //  this.dialogRef.close({ data: 'abc' });
  }

  openFailureSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 6000,
      panelClass: ['red-snackbar'],
    });
  }

  openSuccessSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 6000,
      panelClass: ['green-snackbar'],
    });
  }

  onNoClick(): void {
    this.dialogRef.close({ data: 'closed' });
  }

  getUrl(url) {
    return this.sanitizer.bypassSecurityTrustResourceUrl(url)
  }

}
