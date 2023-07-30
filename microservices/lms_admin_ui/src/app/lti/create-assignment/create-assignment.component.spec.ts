import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MatLegacySnackBar as MatSnackBar } from '@angular/material/legacy-snack-bar';
import { CreateAssignmentComponent } from './create-assignment.component';
import { MatLegacyDialogModule,  MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { FormBuilder } from '@angular/forms';
import { NgxSkeletonLoaderModule } from 'ngx-skeleton-loader';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AngularFireModule } from '@angular/fire/compat';
import { environment } from 'src/environments/environment';
import { By } from '@angular/platform-browser';
import { LtiService } from '../service/lti.service';
import { of } from 'rxjs';
import { MatIconModule } from '@angular/material/icon';
import { ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field'; // Import MatFormFieldModule separately
import { MatInputModule } from '@angular/material/input';
import { MatOption, MatOptionModule } from '@angular/material/core';
import { MatSelect, MatSelectModule } from '@angular/material/select';
import { NgxMatDatetimePickerModule, NgxMatNativeDateModule} from '@angular-material-components/datetime-picker';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { HomeService } from 'src/app/home/service/home.service';


describe('CreateAssignmentComponent', () => {
  let component: CreateAssignmentComponent;
  let fixture: ComponentFixture<CreateAssignmentComponent>;
  let ltiService : LtiService;
  let homeService : HomeService;
  const toolList = [
        {
            "name": "Harmonize Google Dev",
            "description": "Test integration with Harmonize google dev tool",
            "tool_url": "https://google-lti-dev-001.customer.42lines.net",
            "tool_login_url": "https://google-lti-dev-001.customer.42lines.net/api/lti/v13/e00bc131ac334bd48e44b63a227f0d57/initiation",
            "public_key_type": "JWK URL",
            "tool_public_key": null,
            "tool_keyset_url": "https://google-lti-dev-001.customer.42lines.net/.well-known/e00bc131ac334bd48e44b63a227f0d57/jwks.json",
            "content_selection_url": "https://google-lti-dev-001.customer.42lines.net/lti/v13/e00bc131ac334bd48e44b63a227f0d57/harmonize/resource/omni/builder",
            "redirect_uris": [
                "https://google-lti-dev-001.customer.42lines.net/api/lti/v13/e00bc131ac334bd48e44b63a227f0d57/target"
            ],
            "enable_grade_sync": false,
            "enable_nrps": true,
            "custom_params": "deepLinkLaunchEndpoint=$ResourceLink.RelaunchURL;timezone=$Person.address.timezone;prevContexts=$Context.id.history",
            "validate_title_for_grade_sync": false,
            "deeplink_type": "Allow everytime",
            "id": "xwsBdJzPESMQWiQw7Plh",
            "client_id": "db5e915d-87a3-49d8-9b3f-ad95c1934705",
            "deployment_id": "d143100f-e817-4e55-b1a4-63fe9016cb3e",
            "issuer": "https://core-learning-services-dev.cloudpssolutions.com",
            "platform_auth_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/authorize",
            "platform_token_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/token",
            "platform_keyset_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/jwks",
            "created_time": "2023-06-07 13:28:45.285146+00:00",
            "last_modified_time": "2023-06-07 13:56:47.149432+00:00"
        },
        {
            "name": "Insribe preprod",
            "description": "Insribe preprod test tool integration",
            "tool_url": "https://preprod.inscribe.education",
            "tool_login_url": "https://preprod.inscribe.education/organizations/asu/lti13/login",
            "public_key_type": "JWK URL",
            "tool_public_key": null,
            "tool_keyset_url": "https://preprod.inscribe.education/oauth2/jwks",
            "content_selection_url": null,
            "redirect_uris": [
                "https://preprod.inscribe.education/organizations/asu/lti13/launch"
            ],
            "enable_grade_sync": false,
            "enable_nrps": false,
            "custom_params": "",
            "validate_title_for_grade_sync": false,
            "deeplink_type": "Allow everytime",
            "id": "Owxks4ehpcd9CydOwtb8",
            "client_id": "88651ff1-f0c0-4870-b8c8-828f5fbb0e2c",
            "deployment_id": "4f551486-9af0-4471-a125-e45db8b68514",
            "issuer": "https://core-learning-services-dev.cloudpssolutions.com",
            "platform_auth_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/authorize",
            "platform_token_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/token",
            "platform_keyset_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/jwks",
            "created_time": "2023-04-06 16:46:44.783228+00:00",
            "last_modified_time": "2023-04-06 16:46:44.783228+00:00"
        },
        {
            "name": "Honorlock QA Tool",
            "description": "Tool integration with QA Honorlock tool",
            "tool_url": "https://qa2.honorlock.com/org/f028b449-12f4-45f0-991a-2a15a218af4a/launch",
            "tool_login_url": "https://qa2.honorlock.com/org/f028b449-12f4-45f0-991a-2a15a218af4a/oidc/login",
            "public_key_type": "JWK URL",
            "tool_public_key": null,
            "tool_keyset_url": "https://qa2.honorlock.com/canvas_1p3_jwks",
            "content_selection_url": "https://qa2.honorlock.com/org/f028b449-12f4-45f0-991a-2a15a218af4a/launch",
            "redirect_uris": [
                "https://qa2.honorlock.com/org/f028b449-12f4-45f0-991a-2a15a218af4a/launch"
            ],
            "enable_grade_sync": false,
            "enable_nrps": null,
            "custom_params": null,
            "validate_title_for_grade_sync": null,
            "deeplink_type": "Not required",
            "id": "dDbYYg9LuYUmLFLyc72l",
            "client_id": "f3077a63-5111-4542-b481-25909fc88720",
            "deployment_id": "0ec2040a-a43a-442c-b186-6080f4844a7a",
            "issuer": "https://core-learning-services-dev.cloudpssolutions.com",
            "platform_auth_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/authorize",
            "platform_token_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/token",
            "platform_keyset_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/jwks",
            "created_time": "2023-02-03 06:08:00.435049+00:00",
            "last_modified_time": "2023-03-01 17:35:55.212836+00:00"
        },
        {
            "name": "Test IMSGlobal tool",
            "description": "Test tool integration",
            "tool_url": "https://lti-ri.imsglobal.org/lti/tools/3463/launches",
            "tool_login_url": "https://lti-ri.imsglobal.org/lti/tools/3463/login_initiations",
            "public_key_type": "JWK URL",
            "tool_public_key": null,
            "tool_keyset_url": "https://lti-ri.imsglobal.org/lti/tools/3463/.well-known/jwks.json",
            "content_selection_url": "https://lti-ri.imsglobal.org/lti/tools/3463/deep_link_launches",
            "redirect_uris": [
                "https://lti-ri.imsglobal.org/lti/tools/3463/deep_link_launches",
                "https://lti-ri.imsglobal.org/lti/tools/3463/launches"
            ],
            "enable_grade_sync": false,
            "enable_nrps": null,
            "custom_params": null,
            "validate_title_for_grade_sync": null,
            "deeplink_type": "Allow everytime",
            "id": "d3JBEKfmFAg1G8rP94f0",
            "client_id": "d64fb8f1-69ae-41e5-be8e-71b599cc7e20",
            "deployment_id": "90fb5e21-b795-43af-8074-bf7f485708d8",
            "issuer": "https://core-learning-services-dev.cloudpssolutions.com",
            "platform_auth_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/authorize",
            "platform_token_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/token",
            "platform_keyset_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/jwks",
            "created_time": "2023-01-13 01:25:03.864665+00:00",
            "last_modified_time": "2023-02-06 08:36:55.456025+00:00"
        },
        {
            "name": "Harmonize tool",
            "description": "Test integration with Harmonize tool",
            "tool_url": "https://harmonize-google-testing.qa.hrmnz.42lines.net",
            "tool_login_url": "https://harmonize-google-testing.qa.hrmnz.42lines.net/api/lti/v13/7e3c33f9297a4df29aa1c8f2bf8caa20/initiation",
            "public_key_type": "JWK URL",
            "tool_public_key": null,
            "tool_keyset_url": "https://harmonize-google-testing.qa.hrmnz.42lines.net/.well-known/7e3c33f9297a4df29aa1c8f2bf8caa20/jwks.json",
            "content_selection_url": "https://harmonize-google-testing.qa.hrmnz.42lines.net/lti/v13/7e3c33f9297a4df29aa1c8f2bf8caa20/harmonize/resource/omni/builder",
            "redirect_uris": [
                "https://harmonize-google-testing.qa.hrmnz.42lines.net/api/lti/v13/7e3c33f9297a4df29aa1c8f2bf8caa20/target"
            ],
            "enable_grade_sync": false,
            "enable_nrps": true,
            "custom_params": "deepLinkLaunchEndpoint=$ResourceLink.RelaunchURL;timezone=$Person.address.timezone;prevContexts=$Context.id.history",
            "validate_title_for_grade_sync": null,
            "deeplink_type": "Allow everytime",
            "id": "Jz9WXCWu0pod5lDaa2q4",
            "client_id": "16cc5a75-8566-467f-a038-ffcb537f7054",
            "deployment_id": "5adf8a11-8693-4eef-b422-85009a918271",
            "issuer": "https://core-learning-services-dev.cloudpssolutions.com",
            "platform_auth_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/authorize",
            "platform_token_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/token",
            "platform_keyset_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/jwks",
            "created_time": "2023-01-09 18:37:55.444490+00:00",
            "last_modified_time": "2023-06-07 13:56:53.311841+00:00"
        },
        {
            "name": "ALEKS",
            "description": "Tool Integration with ALEKS",
            "tool_url": "https://secure.aleks.com/ltia",
            "tool_login_url": "https://secure.aleks.com/ltia",
            "public_key_type": "JWK URL",
            "tool_public_key": null,
            "tool_keyset_url": "https://secure.aleks.com/ltia/jwks",
            "content_selection_url": "https://secure.aleks.com/ltia",
            "redirect_uris": [
                "https://secure.aleks.com/ltia"
            ],
            "enable_grade_sync": true,
            "enable_nrps": true,
            "custom_params": null,
            "validate_title_for_grade_sync": true,
            "deeplink_type": "Allow once per context",
            "id": "46G7Lol0eHx1th4WJEVE",
            "client_id": "75932254-b45d-4004-9d00-6b30aeddd251",
            "deployment_id": "23232fd9-03aa-4a7e-a485-05ef0a99f6c3",
            "issuer": "https://core-learning-services-dev.cloudpssolutions.com",
            "platform_auth_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/authorize",
            "platform_token_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/token",
            "platform_keyset_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/jwks",
            "created_time": "2023-01-05 17:44:27.780816+00:00",
            "last_modified_time": "2023-02-06 08:36:50.422329+00:00"
        }
  ]

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatLegacyDialogModule, HttpClientTestingModule, BrowserAnimationsModule,NgxSkeletonLoaderModule, MatIconModule,
        MatSelectModule, ReactiveFormsModule, MatFormFieldModule, MatInputModule, MatOptionModule, NgxMatDatetimePickerModule,NgxMatNativeDateModule,MatDatepickerModule,
        AngularFireModule.initializeApp(environment.firebase)],
      declarations: [ CreateAssignmentComponent ],
      providers: [MatSnackBar, FormBuilder, LtiService,
        { provide: MatDialogRef, useValue: jasmine.createSpyObj('MatDialogRef', ['close', 'disableClose']) },
        { provide: MAT_DIALOG_DATA, useValue:  { mode: 'Create', page : 'course_template', init_data: '', extra_data:{"contextId": "ABC" } }},
      ]
    })
    .compileComponents();
    fixture = TestBed.createComponent(CreateAssignmentComponent);
    component = fixture.componentInstance;
    ltiService = TestBed.inject(LtiService);
    homeService = TestBed.inject(HomeService)
    component.dialogData = TestBed.inject(MAT_DIALOG_DATA)
    fixture.detectChanges();
  });

  beforeEach(async()=>{
    const mockResponse = {
      "success": true,
      "message": "Tools has been fetched successfully",
      "data": toolList
    }
    spyOn(ltiService, 'getToolsList').and.returnValue(of(mockResponse))
    component.ngOnInit()
    expect(ltiService.getToolsList).toHaveBeenCalled()
    fixture.detectChanges()
    expect(component.toolsList.length).toBeTruthy()
  })

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have "Create New LTI Assignment" dialog title in Create mode', ()=>{
    const titleElement = fixture.debugElement.query(By.css('h2'))
    expect(titleElement.nativeElement.textContent.trim()).toBe("Create New LTI Assignment")
  })

  it('should have "Update LTI Assignment" dialog title in Create mode', ()=>{
    component.dialogData.mode = "Update"
    fixture.detectChanges()
    const titleElement = fixture.debugElement.query(By.css('h2'))
    expect(titleElement.nativeElement.textContent.trim()).toBe("Update LTI Assignment")
  })

  it('select content button should be disabled in create mode initially', ()=>{
    // identify button Select Content and it is disabled
    const select_content_buttonElements = fixture.debugElement.queryAll(By.css('button'))
    const select_content_buttonElement = select_content_buttonElements.find((button) => button.nativeElement.textContent.trim() === "Select Content");
    const select_content_button = select_content_buttonElement.nativeElement as HTMLButtonElement
    expect(select_content_button.disabled).toBeTruthy()
  })

  it('should select tool "Harmonize Google Dev" from dropdown and LTI Content Item Id field button should be enabled', ()=>{
    // identify button Select Content and it is disabled
    const select_content_buttonElements = fixture.debugElement.queryAll(By.css('button'))
    const select_content_buttonElement = select_content_buttonElements.find((button) => button.nativeElement.textContent.trim() === "Select Content");
    const select_content_button = select_content_buttonElement.nativeElement as HTMLButtonElement
    // identify and click on select tool dropdown
    const tool_Element = fixture.debugElement.query(By.css(`mat-select[formControlName='tool_id']`));
    tool_Element.nativeElement.click() 
    fixture.detectChanges()
    // identify "Harmonize Google Dev" option and click
    const tool_OptionElements = fixture.debugElement.queryAll(By.directive(MatOption));
    const desired_Tool_OptionElement = tool_OptionElements.find((option) => option.nativeElement.textContent.trim() === "Harmonize Google Dev");
    const matOption = desired_Tool_OptionElement.componentInstance as MatOption;
    const mockContentItemServiceResponse = {
      "success": true,
      "message": "Data fetched successfully",
      "data": []
    }
    // Selecting tool option triggers onDropdownChange that internally call getContentItems
    spyOn(ltiService, 'getContentItems').and.returnValue(of(mockContentItemServiceResponse))
    matOption.select()
    fixture.detectChanges()
    expect(ltiService.getContentItems).toHaveBeenCalled() 
    expect(select_content_button.disabled).toBeFalsy()       // check button Select Content that it is enabled
    spyOn(component, 'openContentSelector')
    select_content_button.click()     // click on select button should call openContentSelector method
    fixture.detectChanges()
    expect(component.openContentSelector).toHaveBeenCalled()
  })

  it('should select tool "Honorlock QA Tool" from dropdown and "LTI Content Item Id" field button should change to "Create Content Item" and enabled', ()=>{
    // identify button Select Content and it is disabled
    const select_content_buttonElements = fixture.debugElement.queryAll(By.css('button'))
    const select_content_buttonElement = select_content_buttonElements.find((button) => button.nativeElement.textContent.trim() === "Select Content");
    const select_content_button = select_content_buttonElement.nativeElement as HTMLButtonElement
    expect(select_content_button.disabled).toBeTruthy()
    // identify and click on select tool dropdown
    const tool_Element = fixture.debugElement.query(By.css(`mat-select[formControlName='tool_id']`));
    tool_Element.nativeElement.click() 
    fixture.detectChanges()
    // identify "Harmonize Google Dev" option and click
    const tool_OptionElements = fixture.debugElement.queryAll(By.directive(MatOption));
    const desired_Tool_OptionElement = tool_OptionElements.find((option) => option.nativeElement.textContent.trim() === "Honorlock QA Tool");
    const matOption = desired_Tool_OptionElement.componentInstance as MatOption;
    const mockContentItemServiceResponse = {
      "success": true,
      "message": "Data fetched successfully",
      "data": []
    }
    // Selecting tool option triggers onDropdownChange that internally call getContentItems
    spyOn(ltiService, 'getContentItems').and.returnValue(of(mockContentItemServiceResponse))
    matOption.select()
    fixture.detectChanges()
    expect(ltiService.getContentItems).toHaveBeenCalled() 
    const create_content_item_buttonElements = fixture.debugElement.queryAll(By.css('button'))
    const create_content_item_buttonElement = create_content_item_buttonElements.find((button) => button.nativeElement.textContent.trim() === "Create Content Item");
    const create_content_item_button = create_content_item_buttonElement.nativeElement as HTMLButtonElement
    expect(create_content_item_button.disabled).toBeFalsy()       // check button Select Content that it is enabled
    const contentItemResposne = {
      "success": true,
      "message": "Content item has been created successfully",
      "data": {
          "tool_id": "dDbYYg9LuYUmLFLyc72l",
          "content_item_type": "ltiResourceLink",
          "content_item_info": {
              "text": "Tool integration with QA Honorlock tool",
              "url": "https://qa2.honorlock.com/org/f028b449-12f4-45f0-991a-2a15a218af4a/launch",
              "type": "ltiResourceLink",
              "title": "Honorlock QA Tool"
          },
          "context_id": "Sou4qYc543VVPCgwxqOK",
          "id": "fKPDMjHUd3MgrYCwEQSW",
          "created_time": "2023-06-14 11:25:46.600266+00:00",
          "last_modified_time": "2023-06-14 11:25:46.600266+00:00"
      }
    }
    spyOn(ltiService, 'postContentItem').and.returnValue(of(contentItemResposne))
    create_content_item_button.click()     // click on select button should call createContentItem method which internally calls postContentItem
    fixture.detectChanges()
    expect(ltiService.postContentItem).toHaveBeenCalled()
    // Identify lti_content_item_id field and check value that it is same as contentItemResposne data id
    const lti_content_item_idElement = fixture.debugElement.query(By.css(`input[formControlName='lti_content_item_id']`));
    expect(lti_content_item_idElement.nativeElement.value).toBe(contentItemResposne.data.id)
  })

  it('should select tool "Harmonize tool" from dropdown and LTI Content Item Id field button should be enabled', ()=>{
    // identify button Select Content and it is disabled
    const select_content_buttonElements = fixture.debugElement.queryAll(By.css('button'))
    const select_content_buttonElement = select_content_buttonElements.find((button) => button.nativeElement.textContent.trim() === "Select Content");
    const select_content_button = select_content_buttonElement.nativeElement as HTMLButtonElement
    // identify and click on select tool dropdown
    const tool_Element = fixture.debugElement.query(By.css(`mat-select[formControlName='tool_id']`));
    tool_Element.nativeElement.click() 
    fixture.detectChanges()
    // identify "Harmonize Google Dev" option and click
    const tool_OptionElements = fixture.debugElement.queryAll(By.directive(MatOption));
    const desired_Tool_OptionElement = tool_OptionElements.find((option) => option.nativeElement.textContent.trim() === "Harmonize tool");
    const matOption = desired_Tool_OptionElement.componentInstance as MatOption;
    const mockContentItemServiceResponse = {
      "success": true,
      "message": "Data fetched successfully",
      "data": []
    }
    // Selecting tool option triggers onDropdownChange that internally call getContentItems
    spyOn(ltiService, 'getContentItems').and.returnValue(of(mockContentItemServiceResponse))
    matOption.select()
    fixture.detectChanges()
    expect(ltiService.getContentItems).toHaveBeenCalled() 
    expect(select_content_button.disabled).toBeFalsy()       // check button Select Content that it is enabled
    spyOn(component, 'openContentSelector')
    select_content_button.click()     // click on select button should call openContentSelector method
    fixture.detectChanges()
    expect(component.openContentSelector).toHaveBeenCalled()
  })

  it('should check in Create mode all Date field is empty', ()=>{
    const startDateInputElement = fixture.debugElement.query(By.css(`input[formControlName='start_date']`));
    expect(startDateInputElement.nativeElement.value).toBe("")
    const endDateInputElement = fixture.debugElement.query(By.css(`input[formControlName='end_date']`));
    expect(endDateInputElement.nativeElement.value).toBe("")
    const dueDateInputElement = fixture.debugElement.query(By.css(`input[formControlName='due_date']`));
    expect(dueDateInputElement.nativeElement.value).toBe("")
  })

  it('should fill LTI form, submit and observe response of postLtiAssignments', ()=>{
    // Set tool_id
    const tool_Element = fixture.debugElement.query(By.css(`mat-select[formControlName='tool_id']`));
    tool_Element.nativeElement.click() 
    fixture.detectChanges()
    const tool_ElementSelect = tool_Element.componentInstance as MatSelect
    tool_ElementSelect.value = "Harmonize Google Dev";
    tool_ElementSelect.writeValue(tool_ElementSelect.value);
    //Set lti_assignment_title
    const lti_assignment_titleElement = fixture.debugElement.query(By.css(`input[formControlName='lti_assignment_title']`));
    const lti_assignment_titleInput = lti_assignment_titleElement.nativeElement as HTMLInputElement;
    lti_assignment_titleInput.value = "Test Harmonize assignment 2";
    lti_assignment_titleInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();
    // set Toady's date as start_date
    let date:any = new Date()
    date = component.getFormattedDatetime(date)
    const start_dateControl = component.ltiAssignmentForm.get('start_date')
    start_dateControl.setValue(date)
    // set 20 days later date as end_date
    let plusTwenTyDate:any = new Date()
    plusTwenTyDate.setDate(plusTwenTyDate.getDate()+20)
    plusTwenTyDate = component.getFormattedDatetime(plusTwenTyDate)
    const end_dateControl = component.ltiAssignmentForm.get('end_date')
    end_dateControl.setValue(plusTwenTyDate)
    // set Tomorrow's date as due_date
    let tomorrowDate:any = new Date()
    tomorrowDate.setDate(tomorrowDate.getDate()+20)
    tomorrowDate = component.getFormattedDatetime(tomorrowDate)
    const due_dateControl = component.ltiAssignmentForm.get('due_date')
    due_dateControl.setValue(tomorrowDate)

    const max_pointElement = fixture.debugElement.query(By.css(`input[formControlName='max_points']`));
    const max_inputComp = max_pointElement.nativeElement as HTMLInputElement;
    max_inputComp.value = '50'
    max_inputComp.dispatchEvent(new Event('input'));
    fixture.detectChanges()
    expect(component.ltiAssignmentForm.value.start_date).toBe(date)
    expect(component.ltiAssignmentForm.value.end_date).toBe(plusTwenTyDate)
    expect(component.ltiAssignmentForm.value.due_date).toBe(tomorrowDate)
    expect(component.ltiAssignmentForm.value.max_points).toBe('50')

    const submitButtonElement = fixture.debugElement.query(By.css('button[type="submit"]'));
    spyOn(homeService, 'postLtiAssignments').and.returnValue(of({success:true}))
    submitButtonElement.nativeElement.click()
    fixture.detectChanges()
    expect(homeService.postLtiAssignments).toHaveBeenCalled()
  })

  it('should fill form in update mode and tool_id be disabled, form should be valid and on submit observe response of updateLtiAssignments',()=>{
    const mockData = {
      "id": "IdpXgN3UODfmTlqibMKl",
      "context_id": "cNcuWUQ0VdidE7s9zcA",
      "context_type": "course_template",
      "lti_assignment_title": "Quiz 1 (Aleks)",
      "lti_content_item_id": "zr0mfn2CqpAeUddaqBT",
      "tool_id": "46G7Lol0eHx1th4WJEVE",
      "course_work_id": "6135897136",
      "course_work_type": "course_work",
      "max_points": 30.0,
      "start_date": "2023-04-01T00:00:00+00:00",
      "end_date": "2023-06-17T00:00:00+00:00",
      "due_date": "2023-06-24T00:00:00+00:00"
    }
    component.dialogData.extra_data.assignment = mockData 
    component.dialogData.mode = 'Update'
    component.ngOnInit()
    fixture.detectChanges()
    const tool_idElement = fixture.debugElement.query(By.css('input[formControlName="tool_id"]'))
    const tool_idInput = tool_idElement.nativeElement as HTMLInputElement;
    expect(tool_idInput.disabled).toBeTruthy()
    // Set lti_assignment_title to empty
    const lti_assignment_titleElement = fixture.debugElement.query(By.css('input[formControlName="lti_assignment_title"]'))
    const ltiEle = lti_assignment_titleElement.nativeElement as HTMLInputElement;
    ltiEle.value = ""
    ltiEle.dispatchEvent(new Event('input'))
    fixture.detectChanges()
    expect(component.ltiAssignmentForm.valid).toBeFalse()
    ltiEle.value = "Quiz (Aleks)"
    ltiEle.dispatchEvent(new Event('input'))
    fixture.detectChanges()
    expect(component.ltiAssignmentForm.valid).toBeTruthy()
    const submitButtonElement = fixture.debugElement.query(By.css('button[type="submit"]'));
    spyOn(homeService, 'updateLtiAssignments').and.returnValue(of({success:true}))
    submitButtonElement.nativeElement.click()
    fixture.detectChanges()
    expect(homeService.updateLtiAssignments).toHaveBeenCalled()
  })

});
