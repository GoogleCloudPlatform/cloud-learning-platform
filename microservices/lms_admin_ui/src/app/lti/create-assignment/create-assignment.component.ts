import { Component, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { LtiService } from '../service/lti.service';
import { MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { ContentSelectorComponent } from '../content-selector/content-selector.component';
import { HomeService } from 'src/app/home/service/home.service';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { AuthService } from 'src/app/shared/service/auth.service';
interface LooseObject {
  [key: string]: any
}
@Component({
  selector: 'app-create-assignment',
  templateUrl: './create-assignment.component.html',
  styleUrls: ['./create-assignment.component.scss']
})
export class CreateAssignmentComponent {
  ltiAssignmentForm: FormGroup;
  toolsList = []
  showProgressSpinner: boolean = false
  toolSelectDisabled: boolean = false
  isDisplayButtonEnabled: boolean = false
  isLoading: boolean = true
  displayButton: string = "selectContentItem"
  selectedTool: any
  toolName: any
  constructor(
    private _snackBar: MatSnackBar,
    public dialogRef: MatDialogRef<CreateAssignmentComponent>,
    @Inject(MAT_DIALOG_DATA) public dialogData: any,
    public dialog: MatDialog,
    private fb: FormBuilder, private homeService: HomeService, private ltiService: LtiService, private authService: AuthService) { }

  ngOnInit() {
    console.log('dialog data', this.dialogData)
    this.ltiService.getToolsList().subscribe((res: any) => {
      this.toolsList = res.data
      if (this.dialogData.mode == "Create") {
        this.ltiAssignmentForm = this.fb.group({
          "tool_id": [null, Validators.required],
          "lti_assignment_title": [null, Validators.required],
          "lti_content_item_id": [null],
          "start_date": [null],
          "end_date": [null],
          "due_date": [null],
          "max_points": [null]
        });
      } else {
        this.ltiAssignmentForm = this.fb.group({
          "tool_id": [{value:this.dialogData.extra_data.assignment.tool_id, disabled: true} , Validators.required],
          "lti_assignment_title": [this.dialogData.extra_data.assignment.lti_assignment_title, Validators.required],
          "lti_content_item_id": [this.dialogData.extra_data.assignment.lti_content_item_id],
          "start_date": [this.dialogData.extra_data.assignment.start_date ? this.getFormattedDatetime(this.dialogData.extra_data.assignment.start_date) : null],
          "end_date": [this.dialogData.extra_data.assignment.end_date ? this.getFormattedDatetime(this.dialogData.extra_data.assignment.end_date) : null],
          "due_date": [this.dialogData.extra_data.assignment.due_date ? this.getFormattedDatetime(this.dialogData.extra_data.assignment.due_date) : null],
          "max_points": [this.dialogData.extra_data.assignment.max_points]
        });
        this.toolSelectDisabled = true
        let tool = this.toolsList.find((x) => {
          if (x.id == this.dialogData.extra_data.assignment.tool_id) {
            return true
          }
          return false
        })
        this.toolName = tool.name
        if (tool.deeplink_type == "Not required") {
          this.displayButton = "createContentItem"
          this.isDisplayButtonEnabled = false
        }
      }
      this.isLoading = false
    }, err => {
      this.openFailureSnackBar("Failed to load tools", "Error")
    })
  }

  onDropdownChange() {
    let tool = this.toolsList.find((x) => {
      if (x.id == this.ltiAssignmentForm.value['tool_id']) {
        return true
      }
      return false
    })
    this.ltiAssignmentForm.get("lti_content_item_id").setValue(null)
    this.ltiService.getContentItems(this.ltiAssignmentForm.value['tool_id'], this.dialogData.extra_data.contextId).subscribe(
      (response: any) => {
        if (tool.deeplink_type == "Allow once per context") {
          this.displayButton = "selectContentItem"
          if (response.data.length) {
            this.isDisplayButtonEnabled = false
            this.ltiAssignmentForm.get("lti_content_item_id").setValue(response.data[0].id)
          } else {
            this.isDisplayButtonEnabled = true
          }
        } else if (tool.deeplink_type == "Not required") {
          this.displayButton = "createContentItem"
          if (response.data.length) {
            this.isDisplayButtonEnabled = false
            this.ltiAssignmentForm.get("lti_content_item_id").setValue(response.data[0].id)
          } else {
            this.isDisplayButtonEnabled = true
          }
        } else {
          this.displayButton = "selectContentItem"
          this.isDisplayButtonEnabled = true
        }
      }
    )
  }

  processFormInputs(values) {
    // convert redirect uris from str to list and make data ready to send to API
    const arr = values.redirect_uris.split(";")
    const redirect_uris = arr.map(element => {
      return element.trim();
    });
    const finalValues = { ...values, "redirect_uris": redirect_uris }
    return finalValues
  }

  onSubmit(ltiAssignmentForm) {
    this.showProgressSpinner = true
    const data = ltiAssignmentForm.value
    let context_type = this.dialogData.page
    if (this.dialogData.mode == "Create") {
      this.homeService.postLtiAssignments({ ...data, context_type: context_type, context_id: this.dialogData.extra_data.contextId }).subscribe((response: any) => {
        if (response.success == true) {
          console.log("response", response)
          this.dialogRef.close({ data: 'success' })
        }
        else {
          this.openFailureSnackBar(response?.message, 'FAILED')
        }
        this.showProgressSpinner = false
      })
    } else {
      console.log("this.dialogData.extra_data", this.dialogData.extra_data)
      this.homeService.updateLtiAssignments(this.dialogData.extra_data.assignment.id, data).subscribe((response: any) => {
        console.log("response", response)
        if (response.success == true) {
          this.dialogRef.close({ data: 'success' })
        }
        else {
          this.openFailureSnackBar(response?.message, 'FAILED')
        }
        this.showProgressSpinner = false
      })
    }
  }

  fetchData(id) {
    const data = this.ltiService.getToolData(id).subscribe((response: any) => {
      return response.data
    })
  }

  openFailureSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 6000,
      panelClass: ['red-snackbar'],
    });
  }

  getFormattedDatetime(dateString) {
    const d = new Date(dateString);
    let month = '' + (d.getMonth() + 1);
    let day = '' + d.getDate();
    const year = d.getFullYear();
    let hour = '' + d.getHours();
    let min = '' + d.getMinutes();
    let sec = '' + d.getSeconds();
    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;
    if (hour.length < 2) hour = '0' + hour;
    if (min.length < 2) min = '0' + min;
    if (sec.length < 2) sec = '0' + sec;
    return [year, month, day].join('-') + 'T' + [hour, min, sec].join(':');
  }

  openContentSelector() {
    let userId = null
    if (localStorage.getItem("userId")) {
      userId = localStorage.getItem("userId")
    } else {
      this.authService.findEmailSetId()
      userId = localStorage.getItem("userId")
    }
    if (this.ltiAssignmentForm.value['tool_id'] != null) {
      let ltiModalData: LooseObject = {}
      ltiModalData['mode'] = 'Open'
      ltiModalData['init_data'] = ''
      ltiModalData['extra_data'] = {
        contextId: this.dialogData.extra_data.contextId,
        contextType: this.dialogData.page,
        toolId: this.ltiAssignmentForm.value['tool_id'],
        userId: userId
      }

      const dialogRef = this.dialog.open(ContentSelectorComponent, {
        minWidth: '750px',
        data: ltiModalData
      });

      dialogRef.afterClosed().subscribe(result => {
        if (result.data) {
          this.ltiAssignmentForm.get("lti_content_item_id").setValue(result.data.response[0].content_item_id)
        }
        console.log("result", result)
      });
    }
    else {
      this.openFailureSnackBar('Please select a tool', 'Error')
    }
  }

  createContentItem() {
    let tool = this.toolsList.find((x) => {
      if (x.id == this.ltiAssignmentForm.value['tool_id']) {
        return true
      }
      return false
    })

    let data = {
      tool_id: this.ltiAssignmentForm.value['tool_id'],
      context_id: this.dialogData.extra_data.contextId,
      content_item_type: "ltiResourceLink",
      content_item_info: {
        "text": tool.description,
        "title": tool.name,
        "type": "ltiResourceLink",
        "url": tool.tool_url
      },
    }
    this.ltiService.postContentItem(data).subscribe((res: any) => {
      this.isDisplayButtonEnabled = false
      this.ltiAssignmentForm.get("lti_content_item_id").setValue(res.data.id)
    })
  }

  onNoClick(): void {
    this.dialogRef.close({ data: 'closed' });
  }

}
