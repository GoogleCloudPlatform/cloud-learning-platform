import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { MatLegacyDialogModule, MatLegacyDialog as MatDialog, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogRef as MatDialogRef } from '@angular/material/legacy-dialog'
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ToolFormComponent } from './tool-form.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field'; // Import MatFormFieldModule separately
import { MatInputModule } from '@angular/material/input';
import { MatCheckbox, MatCheckboxModule } from '@angular/material/checkbox';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatOption, MatOptionModule } from '@angular/material/core';
import { MatSelect, MatSelectModule } from '@angular/material/select';

import { LtiService } from '../service/lti.service';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { By } from '@angular/platform-browser';
import { of } from 'rxjs';

describe('ToolFormComponent', () => {
  let component: ToolFormComponent;
  let fixture: ComponentFixture<ToolFormComponent>;
  let ltiService: LtiService;
  const mockData = {
    "name": "Harmonize Google Dev",
    "description": "Test integration with Harmonize google dev tool",
    "tool_url": "https://google-lti-dev-01.customer.42lines.net",
    "tool_login_url": "https://google-lti-dev-001.customer.42lines.net/api/lti/v13/e00bc131ac33bd48e44b6a227f0d57/initiation",
    "public_key_type": "JWK URL",
    // "tool_public_key": null,
    "tool_keyset_url": "https://google-lti-dev-001.customer.42lines.net/.well-known/e00bc131ac33bd48e44b6a227f0d57/jwks.json",
    "deeplink_type": "Allow everytime",
    "content_selection_url": "https://google-lti-dev-001.customer.42lines.net/lti/v13/e00bc131ac33bd48e44b6a227f0d57/harmonize/resource/omni/builder",
    "redirect_uris": [
        "https://google-lti-dev-001.customer.42lines.net/api/lti/v13/e00bc131ac33bd48e44b6a227f0d57/target"
    ],
    "enable_grade_sync": true,
    "enable_nrps": true,
    "custom_params": "deepLinkLaunchEndpoint=$ResourceLink.RelaunchURL;timezone=$Person.address.timezone;prevContexts=$Context.id.history",
    "validate_title_for_grade_sync": false,
    // "id": "xwsBdJzPESMQWiQw7Plh",
    // "client_id": "db5e95d-87a3-49d8-9b3f-ad95c194705",
    // "deployment_id": "d14300f-e817-4e55-b1a4-63fe906cb3e",
    // "issuer": "https://core-learning-services-dev.cloudpssolutions.com",
    // "platform_auth_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/authorize",
    // "platform_token_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/token",
    // "platform_keyset_url": "https://core-learning-services-dev.cloudpssolutions.com/lti/api/v1/jwks",
    // "created_time": "2023-06-07 13:28:45.285146+00:00",
    // "last_modified_time": "2023-06-07 13:56:47.149432+00:00"
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MatLegacyDialogModule, HttpClientTestingModule, ReactiveFormsModule,MatOptionModule,
        MatFormFieldModule, MatCheckboxModule, MatInputModule, MatIconModule, MatMenuModule, MatSelectModule,BrowserAnimationsModule],
      declarations: [ ToolFormComponent ],
      providers: [FormBuilder,FormControl, Validators,
        { provide: MatDialogRef, useValue: jasmine.createSpyObj('MatDialogRef', ['close']) },
        { provide: MAT_DIALOG_DATA, useValue:  { mode: 'Create', init_data: '', extra_data:{} }}
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ToolFormComponent);
    component = fixture.componentInstance;
    ltiService = TestBed.inject(LtiService)
    component.dialogData = TestBed.inject(MAT_DIALOG_DATA)
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have "Create Tool" title in create mode',()=>{
    // create tool heading
    const headingElement = fixture.debugElement.query(By.css('h1'))
    expect(headingElement.nativeElement.textContent.trim()).toBe('Create Tool')
  })

  it('should identify elements and input values in the form in create mode call postTool method and when clicked save ' ,()=>{
    // insert in name input field
    const nameElement = fixture.debugElement.query(By.css(`input[formControlName='name']`));
    const nameInput = nameElement.nativeElement as HTMLInputElement;
    nameInput.value =  mockData.name;
    nameInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    // insert in description input field
    const descriptionElement = fixture.debugElement.query(By.css(`input[formControlName='description']`));
    const descriptionInput = descriptionElement.nativeElement as HTMLInputElement;
    descriptionInput.value =  mockData.description;
    descriptionInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    // insert in tool_url input field
    const tool_urlElement = fixture.debugElement.query(By.css(`input[formControlName='tool_url']`));
    const tool_urlInput = tool_urlElement.nativeElement as HTMLInputElement;
    tool_urlInput.value =  mockData.tool_url;
    tool_urlInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    // insert in tool_login_url input field
    const tool_login_urlElement = fixture.debugElement.query(By.css(`input[formControlName='tool_login_url']`));
    const tool_login_urlInput = tool_login_urlElement.nativeElement as HTMLInputElement;
    tool_login_urlInput.value =  mockData.tool_login_url;
    tool_login_urlInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();
    
    // By default 'JWK URL' option selected for public_key_type
    const public_key_typeElement = fixture.debugElement.query(By.css(`mat-select[formControlName='public_key_type']`));
    const public_key_typeInput = public_key_typeElement.componentInstance as MatSelect;
    const public_key_typeValue =  mockData.public_key_type;
    const selectedValue = public_key_typeInput.value;
    expect(selectedValue).toEqual(public_key_typeValue);

    //Insert in tool_keyset_url input field
    const tool_keyset_url = fixture.debugElement.query(By.css(`input[formControlName='tool_keyset_url']`));
    const tool_keyset_urlInput = tool_keyset_url.nativeElement as HTMLInputElement;
    tool_keyset_urlInput.value =  mockData.tool_keyset_url;
    tool_keyset_urlInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    //Insert in content_selection_url input field
    const content_selection_urlElement = fixture.debugElement.query(By.css(`input[formControlName='content_selection_url']`));
    const content_selection_urlInput = content_selection_urlElement.nativeElement as HTMLInputElement;
    content_selection_urlInput.value =  mockData.content_selection_url;
    content_selection_urlInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    // select option 'Allow Everytime' for deeplink type
    const deeplink_typeElement = fixture.debugElement.query(By.css(`mat-select[formControlName='deeplink_type']`));
    deeplink_typeElement.nativeElement.click()
    fixture.detectChanges()
    const deeplink_typeInput = deeplink_typeElement.componentInstance as MatSelect;
    const deeplink_typeValue =  mockData.deeplink_type;
    const deeplink_typeOptions = fixture.debugElement.queryAll(By.directive(MatOption));
    // Find and select the deeplink_typedesired option
    const deeplink_typedesiredOption = deeplink_typeOptions.find((option) => option.nativeElement.textContent.trim() === deeplink_typeValue);
    deeplink_typeInput.value = deeplink_typedesiredOption.componentInstance.value;
    deeplink_typeInput.writeValue(deeplink_typeInput.value);
    fixture.detectChanges();

    //Insert in redirect_uris textarea 
    const redirect_urisElement = fixture.debugElement.query(By.css(`textarea[formControlName='redirect_uris']`));
    const redirect_urisInput = redirect_urisElement.nativeElement as HTMLTextAreaElement;
    let redirectUris:any = mockData.redirect_uris;
    if (typeof (redirectUris) == "object") {
      redirectUris = redirectUris.join(";")
    }
    redirect_urisInput.value =  redirectUris;
    redirect_urisInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    //Insert in redirect_uris textarea 
    const custom_paramsElement = fixture.debugElement.query(By.css(`textarea[formControlName='custom_params']`));
    const custom_paramsInput = custom_paramsElement.nativeElement as HTMLTextAreaElement;
    custom_paramsInput.value =  mockData.custom_params;
    custom_paramsInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();

    //debug enable_grade_sync and verify it's value is false and change it to true
    const enable_grade_syncElement = fixture.debugElement.query(By.css('mat-checkbox[formControlName="enable_grade_sync"]'));
    const enable_grade_syncComponent = enable_grade_syncElement.componentInstance as MatCheckbox;
    expect(enable_grade_syncComponent.checked).toBeFalse()
    enable_grade_syncComponent.toggle()
    fixture.detectChanges();
    expect(enable_grade_syncComponent.checked).toBeTrue()

    //debug enable_nrps and verify it's value is false and change it to true
    const enable_nrpsElement = fixture.debugElement.query(By.css('mat-checkbox[formControlName="enable_nrps"]'));
    const enable_nrpsComponent = enable_nrpsElement.componentInstance as MatCheckbox;
    expect(enable_nrpsComponent.checked).toBeFalse()
    enable_nrpsComponent.toggle()
    fixture.detectChanges();
    expect(enable_nrpsComponent.checked).toBeTrue()

    //debug validate_title_for_grade_sync and verify it's value is false 
    const validate_title_for_grade_syncElement = fixture.debugElement.query(By.css('mat-checkbox[formControlName="validate_title_for_grade_sync"]'));
    const validate_title_for_grade_syncComponent = validate_title_for_grade_syncElement.componentInstance as MatCheckbox;
    expect(validate_title_for_grade_syncComponent.checked).toBeFalse()

    // Identify save button and click
    const submitElement = fixture.debugElement.query(By.css('button[type="submit"]'));
    spyOn(ltiService, 'postTool').and.returnValue(of({success:true}))
    submitElement.nativeElement.click()
    fixture.detectChanges();
    // Check whether postTool method is called when clicked on Save button
    expect(ltiService.postTool).toHaveBeenCalled()
    const subData = component.processFormInputs(component.toolForm.value)
    expect(JSON.stringify(mockData)).toEqual(JSON.stringify(subData))
  })

  it('should have "Update Tool" title in Update mode',()=>{
    // Update Tool heading
    component.dialogData = {...component.dialogData, mode : 'Update'}
    fixture.detectChanges()
    const headingElement = fixture.debugElement.query(By.css('h1'))
    expect(headingElement.nativeElement.textContent.trim()).toBe('Update Tool')
  })

  it('should insert all form fields in Edit mode and call updateTool when clicked save button', ()=>{
    component.dialogData = {...component.dialogData, extra_data : mockData, mode : 'Update'}
    component.ngOnInit()
    fixture.detectChanges()
    const headingElement = fixture.debugElement.query(By.css('h1'))
    expect(headingElement.nativeElement.textContent.trim()).toBe('Update Tool')
    // check all field value
    const nameElement = fixture.debugElement.query(By.css(`input[formControlName='name']`));
    expect(nameElement.nativeElement.value).toBe(mockData.name)
    const descriptionElement = fixture.debugElement.query(By.css(`input[formControlName='description']`));
    expect(descriptionElement.nativeElement.value).toBe(mockData.description)
    const tool_urlElement = fixture.debugElement.query(By.css(`input[formControlName='tool_url']`));
    expect(tool_urlElement.nativeElement.value).toBe(mockData.tool_url)
    const tool_login_urlElement = fixture.debugElement.query(By.css(`input[formControlName='tool_login_url']`));
    expect(tool_login_urlElement.nativeElement.value).toBe(mockData.tool_login_url)
    const public_key_typeElement = fixture.debugElement.query(By.css(`mat-select[formControlName='public_key_type']`));
    expect(public_key_typeElement.nativeElement.textContent).toBe(mockData.public_key_type)
    const tool_keyset_url = fixture.debugElement.query(By.css(`input[formControlName='tool_keyset_url']`));
    expect(tool_keyset_url.nativeElement.value).toBe(mockData.tool_keyset_url)
    const content_selection_urlElement = fixture.debugElement.query(By.css(`input[formControlName='content_selection_url']`));
    expect(content_selection_urlElement.nativeElement.value).toBe(mockData.content_selection_url)
    const deeplink_typeElement = fixture.debugElement.query(By.css(`mat-select[formControlName='deeplink_type']`));
    expect(deeplink_typeElement.nativeElement.textContent).toBe(mockData.deeplink_type)
    const redirect_urisElement = fixture.debugElement.query(By.css(`textarea[formControlName='redirect_uris']`));
    const uris = redirect_urisElement.nativeElement.value.split(";").map(element => element.trim());
    expect(uris).toEqual(mockData.redirect_uris)
    const custom_paramsElement = fixture.debugElement.query(By.css(`textarea[formControlName='custom_params']`));
    expect(custom_paramsElement.nativeElement.value).toBe(mockData.custom_params)
    const enable_grade_syncElement = fixture.debugElement.query(By.css('mat-checkbox[formControlName="enable_grade_sync"]'));
    const enable_grade_syncComponent = enable_grade_syncElement.componentInstance as MatCheckbox;
    expect(enable_grade_syncComponent.checked).toBe(mockData.enable_grade_sync)
    const enable_nrpsElement = fixture.debugElement.query(By.css('mat-checkbox[formControlName="enable_nrps"]'));
    const enable_nrpsComponent = enable_nrpsElement.componentInstance as MatCheckbox;
    expect(enable_nrpsComponent.checked).toBe(mockData.enable_nrps)
    const validate_title_for_grade_syncElement = fixture.debugElement.query(By.css('mat-checkbox[formControlName="validate_title_for_grade_sync"]'));
    const validate_title_for_grade_syncComponent =  validate_title_for_grade_syncElement.componentInstance as MatCheckbox;
    expect(validate_title_for_grade_syncComponent.checked).toBe(mockData.validate_title_for_grade_sync)
    const submitElement = fixture.debugElement.query(By.css('button[type="submit"]'));
    spyOn(ltiService, 'updateTool').and.returnValue(of({success:true}))
    submitElement.nativeElement.click()
    fixture.detectChanges();
    // Check whether updateTool method is called when clicked on Save button
    expect(ltiService.updateTool).toHaveBeenCalled()
  })

  it('should toggle tool_public_key/tool_keyset_url formcontrol on public_key_type change',()=>{
    // for public_key_type "JKW URL" formControl tool_keyset_url should be available
    const tool_keyset_url = fixture.debugElement.query(By.css(`input[formControlName='tool_keyset_url']`));
    expect(tool_keyset_url).toBeTruthy() 
    // identify and click on public_key_type select dropdown
    const publiKeyType_Element = fixture.debugElement.query(By.css(`mat-select[formControlName='public_key_type']`));
    publiKeyType_Element.nativeElement.click() 
    fixture.detectChanges()
    // identify "Public Key" option and click
    const publiKeyType_OptionElement = fixture.debugElement.query(By.css('mat-option[value="Public Key"]'))
    const matOption = publiKeyType_OptionElement.componentInstance as MatOption;
    matOption.select()
    fixture.detectChanges()
    // for public_key_type "Public Key" formControl tool_public_key should be available
    const tool_public_key = fixture.debugElement.query(By.css(`textarea[formControlName='tool_public_key']`));
    expect(tool_public_key).toBeTruthy() 
  })
});
