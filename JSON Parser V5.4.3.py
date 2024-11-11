import json
import decimal as d
import xml.etree.ElementTree as ET
import datetime as dt

# Nombre del archivo JSON
nombre_archivo = "JSON File route.json"

# Intentar abrir y leer el archivo JSON
with open(nombre_archivo, 'r', encoding="utf8") as archivo:
    # Cargar el contenido JSON
    contenido_json = json.load(archivo)
    print("Fichero Procesado: ", nombre_archivo)

    #Elegimos el Escenario por el que pasar:

    #Placement Cancelled (Renewals).
    if contenido_json.get("placementStatusId") == 6 and (contenido_json.get("opportunityTypeId") != 168 or contenido_json.get("opportunityTypeId") != 173) :

        print("\tPlacement_type:" , contenido_json.get("placementStatus"))

        print("\tPolizas a Anular en Gestmat:")
        #PolId Elevia/Gestmat:

        pols_can = [iz for iz in contenido_json.get("policies")]

        for i in pols_can:    
            try:
                root = ET.fromstring(i.get("policyAttributeXML"))
                print("\t\t\t- ",root.find('POL_ID').text)
            except:
                print("\t\t\t- Error, No se encontro POL ID para la POL REF: ",i.get("policyReference") , ", proceda a cancelarla manualmente.")

        #Comenrario Cancelación:
        can_com = contenido_json.get("instructionDetails")
        print("\t\t\t- Comments: ", can_com)

    #Tacit Renewal.
    elif contenido_json.get("placementStatusId") == 3 and contenido_json.get("opportunityTypeId") == 169 and (contenido_json.get("appraisalTypeId") == 5 or contenido_json.get("appraisalTypeId") == 6 ):
        
        print("\tPlacement_type:" , contenido_json.get("appraisalType"), contenido_json.get("opportunityType") )

        print("\tPolizas a Marcar cómo Tacitas en GestMat:")
        #PolId of Local Servicing Platform:

        pols_tacit = [iz for iz in contenido_json.get("policies") if iz.get("placementPolicyRelationshipTypeId") == 2]

        for i in pols_tacit:    
            try:
                root = ET.fromstring(i.get("policyAttributeXML"))
                print("\t\t\t- ",root.find('POL_ID').text)
            except:
                print("\t\t\t- Error, No se encontro POL ID para la POL REF: ",i.get("policyReference"),", proceda a renovarla manualmente.")
        
        #Comenrario Cancelación:
        tac_com = contenido_json.get("instructionDetails")
        print("\t\t\t- Comments: ", tac_com)

    #Placement Complete (New Business + Renewal + AT(Marketing or Not Remarketing))
    elif contenido_json.get("placementStatusId") == 3 and contenido_json.get("appraisalTypeId") != 5 and contenido_json.get("appraisalTypeId") != 6 :

        print("\tPlacement_type:" ,  contenido_json.get("opportunityType") ,contenido_json.get("appraisalType"))

        #NumeroPólizasAGenerar
        respuestas=contenido_json.get("negotiations")[0].get("negotiationMarkets");
        #print("Nº de respuestas: ", len(respuestas))
        rskp=contenido_json.get("riskProfiles");    
        print("Nº de riskProfiles: ", len(rskp))
        layer_num=contenido_json.get("riskStructures");    
        print("Nº de riskStructures: ", len(layer_num))
	

        CliId=[cli for cli in contenido_json.get("placementPartyRoles") if (cli["partyTypeDescription"]=="Client" and cli["onPlacement"]==True)][0].get("globalPartyId")
        CliName=[cli for cli in contenido_json.get("placementPartyRoles") if (cli["partyTypeDescription"]=="Client" and cli["onPlacement"]==True)][0].get("name")

	    #Itero por los riskProfiles
        
        num_poliza = 0
        for rskpItem in rskp:
            riskProfileId=rskpItem.get("riskProfileId");
            print("\tRiskProfileId" , riskProfileId);
            descripRiesgo=rskpItem.get("classOfBusiness");
            descripLinea=rskpItem.get("lineOfBusiness");
            ProdId=rskpItem.get("productId");
            classOfBusinessId=rskpItem.get("classOfBusinessId");
            lineOfBusinessId=rskpItem.get("lineOfBusinessId");
            classOfBusinessId=rskpItem.get("classOfBusinessId");
            lineOfBusinessId=rskpItem.get("lineOfBusinessId");
        
            layer_basket =[i.get("riskStructureId") for i in contenido_json.get("riskStructures") if i.get("riskProfileId") == riskProfileId ]
            layers = list(set(layer_basket))
            
            #Negociaciones Current:
            currents = [i for i in contenido_json.get("negotiations") if i.get("negotiationType")=="Current"]
            l_cur = len(currents)
            
            #Itero por las Negociaciones "Current"
            for j in range(0,l_cur):
                responsesN1 = [resp for resp in currents[j].get("negotiationMarkets")]
                print("\tNegotiation:", currents[j].get("negotiationName"))
                
                #  Itero por los riskStructures (layers)
                for layer in layers: 
                        #Itero por las respuestas dentro de la layer
                        for rn1 in responsesN1:
                            try:
                                responsesN2 = [resp for resp in rn1.get("negotiationMarketResponses") if(resp.get("marketResponseBasis")[0].get("riskProfileId")==riskProfileId and resp.get("outcomeStatusId")==1 and resp.get("responseTypeId")==1 and resp.get("riskStructureId")==layer)]
                            except:
                                responsesN2 = []

                            for rn2 in responsesN2: 
                        
                            #Numero la Poliza o coaseguro
    
                                lider = rn2.get("quotedToLead")
                                print("\t\triskStructureId" , rn2.get("riskStructureId"), end='');
                                layerType =rn2.get("layerType");
                                numPoliza = 0
                                print(" - layerType:" , layerType);
                        
                                if  lider == False:
                                    print("\t\tCoaseguro de Póliza", num_poliza, end='')
                                    print("- Leader: ", rn2.get("quotedToLead"), end='')
                                    print("- % Coaseguro ", rn2.get("signedLineRate"))
                                else:
                                    print("\t\tPóliza ", num_poliza, end='')
                                    print("- Leader: ", rn2.get("quotedToLead"), end='')
                                    print("- % Coaseguro ", rn2.get("signedLineRate"))
                       
    
                                #Identificador Cliente
                                print ("\t\t\tIdentificador Cliente", CliId,"-",CliName)
            
                                #Compañía
                                print("\t\t\tCarrier: ",end ="")
                                print(rn1.get("carrier").get("compCode"), end='')
                                print(' - ', rn1.get("carrier").get("carrierName"))
                
                                #Tipo Poliza (NUEVO, ETKey)
                                try:
                                    print("\t\t\tTipo Poliza: ", [aux1 for aux1 in rn2.get("marketResponseAttributes") if 
        (aux1["elementAttributeTypeId"]==811 and aux1["elementTypeKey"]== "responseCapture_metric_policyType")][0].get("displayValue"))
                                except:
                                    print("\t\t\t","!!!!!!!!!!!ERROR","-Tipo Poliza: VACIO","-ERROR!!!!!!!!!!!!!")
                        
                                #Roles
                                #1.-Ejecutivo
                                try:
                                    print("\t\t\tEjecutivo: ", [aux1 for aux1 in 
        contenido_json.get("placementServicingRole") if (aux1["servicingRoleId"]==10)][0].get("email"))
                                except:
                                    print("\t\t\tEjecutivo: NONE")
                                
                                #2.-Placement Creator (NUEVO, Email Main Broker) *
                                try:
                                    print("\t\t\tPlacement Creator: ", [aux1 for aux1 in 
        contenido_json.get("placementServicingRole") if (aux1["servicingRoleId"]==22)][0].get("email"))
                                except:
                                    print("\t\t\tPlacement Creator: ", currents[j].get("contactEmail"))
                            
                                
                                #Oficina
                                print("\t\t\tOficina: ", contenido_json.get("brokingRegionId"))
                                print("\t\t\tOpportunityType: ", contenido_json.get("opportunityTypeId"))
                                print("\t\t\trenewableOptionId: ", contenido_json.get("renewableOptionId"))
                                print("\t\t\tappraisalTypeId: ", contenido_json.get("appraisalTypeId"))
                
                                #Team
                                print("\t\t\tTeam: ", contenido_json.get("teamId"),";",contenido_json.get("teamDescription")), 
                                print("\t\t\t\tRegion_Id: ", contenido_json.get("brokingRegionId"),";",contenido_json.get("brokingRegion"))
                                #print("\t\t\t\tTeam-industryId: ", contenido_json.get("industryId"))
                                #print("\t\t\t\tTeam-brokingSegmentId: ", contenido_json.get("brokingSegmentId")) 
            
                                #Duraccion
                                print("\t\t\tRenewable_Option: ", contenido_json.get("renewableOption"))
    
                                #Ramo
                                print("\t\t\tProduct Id", ProdId , ":")
                                print("\t\t\t\tClass Of Business Id", classOfBusinessId,";",descripRiesgo)
                                print("\t\t\t\tLine Of Business Id", lineOfBusinessId,";",descripLinea)

                                #DescripcionRiesgo, (NUEVO, ETKey)
                                try:
                                     print("\t\t\tDescripcionRiesgo: ", [aux1 for aux1 in 
        rn2.get("marketResponseAttributes") if (aux1["elementAttributeTypeId"]==360 and aux1["elementTypeKey"]=="responseCapture_metric_businessDescription")][0].get("value"))
                                except:
                                     print("\t\t\tDescripcionRiesgo:", descripRiesgo)

                                #FechaEfecto (NUEVO, ETKey)
                                print("\t\t\tFechaEfecto: ", [aux1 for aux1 in rn2.get("marketResponseAttributes") if 
        (aux1["elementAttributeTypeId"]==343 and aux1["elementTypeKey"]=="responseCapture_metric_limit_policyEffectiveDate")][0].get("value")[0:10])
            
                                #FechaVencimiento (NUEVO, ETKey)
                                exp_date = [aux1 for aux1 in rn2.get("marketResponseAttributes") if 
        (aux1["elementAttributeTypeId"]==343 and aux1["elementTypeKey"]=="responseCapture_metric_limit_policyExpiryDate")][0].get("value")[0:10]
                                exp_date = dt.datetime.strptime(exp_date, "%Y-%m-%d").date()
                                exp_hour = dt.datetime.strptime(contenido_json.get("expiryStartTime"), "%H:%M").hour
                                
                                if exp_hour >=23:
                                    exp_date += dt.timedelta(days=1)
                                    print("\t\t\tFechaVencimiento: ", exp_date)
                                else:
                                    print("\t\t\tFechaVencimiento: ", exp_date)
    
                                #PeriodicidadPago (NUEVO, ETKey)
                        
                                try:
                                    print("\t\t\tPeriodicidadPago: ", [aux1 for aux1 in rn2.get("marketResponseAttributes") 
        if (aux1["elementAttributeTypeId"]==636 and aux1["elementTypeKey"]=="responseCapture_metric_premium_instalmentPeriod")][0].get("value"),";",[aux1 for aux1 in rn2.get("marketResponseAttributes") 
        if (aux1["elementAttributeTypeId"]==636 and aux1["elementTypeKey"]=="responseCapture_metric_premium_instalmentPeriod")][0].get("displayValue"))
                                except:
                                    print("\t\t\t","!!!!!!!!!!!ERROR","-tPeriodicidadPago: VACIO ","-ERROR!!!!!!!!!!!!!")
                                
                                #Moneda (NUEVO, ETKey)
                                try:
                                    print("\t\t\tCodigoMoneda: ", [aux1 for aux1 in rn2.get("marketResponseAttributes") if 
        (aux1["elementAttributeTypeId"]==342 and aux1["elementTypeKey"]=="responseCapture_metric_premium_layer")][0].get("value"))
                                except:
                                    print("\t\t\tCodigoMoneda: ",rn2.get("premiumCurrencyId"))
                        
                                #Moneda
                                print("\t\t\tMoneda: ", rn2.get("premiumCurrencyCode"))
            
                                
    
                                #PrimaNeta
                                print("\t\t\tPrimaNeta: ", rn2.get("premium"))
                    
                                #Comisiones (NUEVO, Amounts based on %)*
                                try:
                                    commis = rn2.get("commission")
                                    if commis is None:
                                        pass
                                    else:
                                        print("\t\t\tComisiones: ", rn2.get("commission"))
                                except:
                                    pass
                                try:
                                    if commis == 0 or commis is None:
                                        print("\t\t\tComisiones:", round(d.Decimal(rn2.get("commissionRate")*rn2.get("premium")/100),2),"[",rn2.get("commissionRate"),"%]")
                                    else:
                                        pass
                                except:
                                    print("\t\t\tComisiones:",0)
            
                                #Consorcio (NUEVO, ETKey + Amounts based on %)*
                                try:
                                    print("\t\t\tConsorcio: ", [aux1 for aux1 in rn2.get("marketResponseAttributes") if (aux1["elementAttributeTypeId"]==337 and aux1["elementTypeKey"]=="responseCapture_metric_consorcioContribution")][0].get("value"))
                                except:
                                    print("\t\t\tConsorcio:", 0)
           
                                #Impuestos (NUEVO, ETKey)*
								
                                #evaluamos imps e imps_per
                                try:
                                    imps = [aux1 for aux1 in rn2.get("marketResponseAttributes") if (aux1["elementAttributeTypeId"]==337 and aux1["elementTypeKey"]=="responseCapture_metric_premium_insurancePremiumTax")][0].get("value")                                
                                except:
                                    imps = 0

                                try:
                                    imps_per = [aux1 for aux1 in rn2.get("marketResponseAttributes") if (aux1["elementAttributeTypeId"]==353 and aux1["elementTypeKey"]=="responseCapture_metric_premium_insurancePremiumTax")][0].get("value")
                                except:
                                    imps_per = 0

                                #Calculamos impuestos

                                if imps == 0:
                                    print("\t\t\tImpuestos: ", round(d.Decimal(float(imps_per)*rn2.get("premium")/100),2),"[",imps_per,"%]")
                                else:
                                    print("\t\t\tImpuestos: ", imps)
                                
                                                                

                                #OtrosImpuestos
                                print("\t\t\tOtrosImpuestos", rn2.get("additionalPolicyCost")) 
    
    
                                #Expiring Policy
                                try:
                                    exp_policyref =[i.get("policyReference") for i in contenido_json.get("policies") if i.get("policyId") == rn2.get("marketResponsePlacementPolicies",{})[0].get("policyId") and i.get("placementPolicyRelationshipTypeId") == 2]
                                    
                                    print("\t\t\tExpiring Policy:",exp_policyref[0])
                                except :
                                    print("\t\t\tExpiring Policy: None")
                                                                
                                #Elementos Elevia/Gestmat:
                                try:
                                    XML_policyid =[i.get("policyAttributeXML") for i in contenido_json.get("policies") if i.get("policyId") == rn2.get("marketResponsePlacementPolicies",{})[0].get("policyId") and i.get("placementPolicyRelationshipTypeId") == 2]
                                    root = ET.fromstring(XML_policyid[0])
                                    print("\t\t\tExpiring Local Pol_id :",root.find('POL_ID').text)
                                except:
                                    print("\t\t\tExpiring Local Pol_id : None",) 

                                #Current Policy (NUEVO, Poliza Actual)
                                try:
                                    cur_policyref =[i.get("policyReference") for i in contenido_json.get("policies") if i.get("policyId") == rn2.get("marketResponsePlacementPolicies",{})[0].get("policyId") and i.get("placementPolicyRelationshipTypeId") == 1]
    
                                    print("\t\t\tCurrent Policy:",cur_policyref[0])
                                except:
                                    print("\t\t\tCurrent Policy: None") 
    
                                #OportunidadAsociada
                                print("\t\t\tOportunidadAsociada: ", contenido_json.get("crmOpportunityId"))

                                #Elementos API Response:
                                print("\t\tELEMENTOS RESPUESTA API - " , end='');
                                print("marketQuoteResponseId" , rn2.get("marketQuoteResponseId"));
                    
                        num_poliza+=1
        num_poliza+=1
    
    #MTA Complete
    elif contenido_json.get("placementStatusId") == 21: 
        
        #Current Data:
        MTAs =[i for i in contenido_json.get("policies") if i.get("placementPolicyRelationshipTypeId") ==  3]
        l_mtas = len(MTAs)
        
        #Validación 1:
        #El MTA contiene más de 1 Poliza:
        if l_mtas > 1 : 
            print("\t\t- Validations:")
            print("\t\t\t- ERROR, The MTA Contains more than 1 Policy.", "[",l_mtas," polices]")
            pass
        else:
            for j in range(0,l_mtas):
                
                #Accedemos a cada negociación:
                adj = [i for i in contenido_json.get("negotiations") if i.get("negotiationType",{})=="Adjustment"]
                his = [i for i in contenido_json.get("negotiations") if i.get("negotiationType",{})=="Historic"]
                exp = [i for i in contenido_json.get("negotiations") if i.get("negotiationType",{})=="Expiring"]    
    
                #Determinamos el Lead_Carrier:
                mta_carrier_list = {}
                descriptions = {}
                
                n_true = len([i for i in adj if i.get("negotiationMarkets",{})[0].get("negotiationMarketResponses")[0].get("quotedToLead") == True])
                if n_true >0:
                    mta_carrier_list = {i.get("negotiationMarkets",{})[0].get("carrier",{}).get("compCode") : [j for j in i.get("negotiationMarkets",{})[0].get("negotiationMarketResponses")[0].get("marketResponseAttributes") if (j["elementAttributeTypeId"]==353 and j["elementTypeKey"]=="responseCapture_metric_signedLineRate")][0].get("value") for i in adj if i.get("negotiationMarkets",{})[0].get("negotiationMarketResponses")[0].get("quotedToLead") == True}
                    descriptions = {i.get("negotiationMarkets",{})[0].get("carrier",{}).get("compCode") : i.get("negotiationMarkets",{})[0].get("carrier",{}).get("carrierName") for i in adj if i.get("negotiationMarkets",{})[0].get("negotiationMarketResponses")[0].get("quotedToLead") == True}    
                    lead_carrier = max(mta_carrier_list, key=mta_carrier_list.get)
                    lead_carrier_perc = mta_carrier_list[lead_carrier]
                    lead_carrier_descp = descriptions[lead_carrier]
                    max_value = max(mta_carrier_list.values())
                    max_count = list(mta_carrier_list.values()).count(max_value)                   
                else:
                    mta_carrier_list = {i.get("negotiationMarkets",{})[0].get("carrier",{}).get("compCode") : [j for j in i.get("negotiationMarkets",{})[0].get("negotiationMarketResponses")[0].get("marketResponseAttributes") if (j["elementAttributeTypeId"]==353 and j["elementTypeKey"]=="responseCapture_metric_signedLineRate")][0].get("value") for i in adj}
                    descriptions = {i.get("negotiationMarkets",{})[0].get("carrier",{}).get("compCode") : i.get("negotiationMarkets",{})[0].get("carrier",{}).get("carrierName") for i in adj}
                    max_value = max(mta_carrier_list.values())
                    max_count  = list(mta_carrier_list.values()).count(max_value)
                    if max_count == 1:
                        lead_carrier = max(mta_carrier_list, key=mta_carrier_list.get)
                        lead_carrier_perc = mta_carrier_list[lead_carrier]
                        lead_carrier_descp = descriptions[lead_carrier]    
                    else:
                        #Validacion 2 - No hay lead flag y existen varios máximos:
                        print("ERROR - There is no leader in the coinsurance and the max % is repeated", max_count, "times.["+max_value+"%]")
                        pass               
                    
                #Identify the Leaders Negotiations Adj, Historic and Expiring:
                if max_count ==1:
                    lead_adj = [i.get("negotiationMarkets",{})[0].get("negotiationMarketResponses")[0] for i in adj if i.get("negotiationMarkets",{})[0].get("carrier",{}).get("compCode") == lead_carrier]
                    lead_his = [i.get("negotiationMarkets",{})[0].get("negotiationMarketResponses")[0]  for i in his if i.get("negotiationMarkets",{})[0].get("carrier",{}).get("compCode")  == lead_carrier]
                    try:
                        lead_exp = [i.get("negotiationMarkets",{})[0].get("negotiationMarketResponses")[0] for i in exp if i.get("negotiationMarkets",{})[0].get("carrier",{}).get("compCode")  == lead_carrier]
                    except:
                        lead_exp = []
                else:
                    break
    
                #Delta Calculations based on the Leader:
    
                for i in lead_adj:
    
                    #Funciones delta:
                    def delta_root(var):
                        adj_amount = lead_adj[0].get(var)
                        his_amount = lead_his[0].get(var)
                        try:
                            exp_amount = lead_exp[0].get(var)
                        except:
                            exp_amount = None
                        
                        
                        if exp_amount is None:
                            if adj_amount is None and his_amount is None:
                                res= 0
                            elif his_amount is None:
                                res = adj_amount
                            elif adj_amount is None:
                                res = his_amount*-1
                            else:
                                res = adj_amount - his_amount
                        else:
                            res = adj_amount - exp_amount
                        return res
        
                    def delta_atributes_amounts(elementTypeKey):
                
                        try:
                            adj_amount= [i for i in lead_adj[0].get("marketResponseAttributes") if (i["elementAttributeTypeId"]==337 and i["elementTypeKey"]==elementTypeKey)][0].get("value")
                        except:
                            adj_amount = 0
                        try:
                            exp_amount=[i for i in lead_exp[0].get("marketResponseAttributes") if (i["elementAttributeTypeId"]==337 and i["elementTypeKey"]==elementTypeKey)][0].get("value")
                        except:
                            exp_amount = None
                        try:
                            his_amount =[i for i in lead_his[0].get("marketResponseAttributes") if (i["elementAttributeTypeId"]==337 and i["elementTypeKey"]==elementTypeKey)][0].get("value")
                        except:
                            his_amount = 0
            
                        if exp_amount is None:
                            if adj_amount is None and his_amount is None:
                                res= 0
                            elif his_amount is None:
                                res = int(adj_amount)
                            elif adj_amount is None:
                                res = int(his_amount)*-1
                            else:
                                res = int(adj_amount) - int(his_amount)
                        else:
                            res = int(adj_amount) - int(exp_amount)
                        return res
                    
                    def delta_atributes_percentages(elementTypeKey):
                        try:
                            adj_perc = [i for i in lead_adj[0].get("marketResponseAttributes") if (i["elementAttributeTypeId"]==353 and i["elementTypeKey"]==elementTypeKey)][0].get("value")
                        except:
                            adj_perc=0
                        try:
                            exp_perc = [i for i in lead_exp[0].get("marketResponseAttributes") if (i["elementAttributeTypeId"]==353 and i["elementTypeKey"]==elementTypeKey)][0].get("value")
                        except:
                            exp_perc=None
                        try:
                            his_perc = [i for i in lead_his[0].get("marketResponseAttributes") if (i["elementAttributeTypeId"]==353 and i["elementTypeKey"]==elementTypeKey)][0].get("value")
                        except:
                            his_perc=0
                           
                        adj_amount = lead_adj[0].get("premium")
                        
                        try:
                            exp_amount = lead_exp[0].get("premium")
                        except:
                            exp_amount = None
                        
                        his_amount = lead_his[0].get("premium")
                        
                        if exp_perc is None:
                            if adj_perc is None and his_perc is None:
                                res= 0
                            elif his_perc is None:
                                res = int(adj_amount)*float(adj_perc)/100
                            elif adj_perc is None:
                                res = -1*int(his_amount)*float(his_perc)/100
                            else:
                                res = int(adj_amount)*float(adj_perc)/100 - int(his_amount)*float(his_perc)/100
                        else:
                            res = int(adj_amount)*float(adj_perc)/100 - int(exp_amount)*float(exp_perc)/100
                        return res
                
                    def basis(days):
                        inception_date = dt.datetime.strptime(contenido_json.get("inceptionDate")[0:10],"%Y-%m-%d")
                        exp_date = dt.datetime.strptime(contenido_json.get("expiryDate")[0:10], "%Y-%m-%d")
                        exp_hour = dt.datetime.strptime(contenido_json.get("expiryStartTime"), "%H:%M").hour
                        if exp_hour >=23:
                                exp_date += dt.timedelta(days=1)
                        xbasis = float((exp_date - inception_date).days/days)
                        return xbasis
                    
                    def is_leap_year(year):
                        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                            return True
                        else:
                            return False
                    
                    #Validación 3:
                    #La expiry date del overview y la respuesta ajustada no son iguales.
    
                    adj_expdate = [i for i in lead_adj[0].get("marketResponseAttributes") if (i["elementAttributeTypeId"]==343 and i["elementTypeKey"]=="responseCapture_metric_limit_policyExpiryDate")][0].get("value")
                    exp_expdate = [i for i in lead_adj[0].get("marketResponseAttributes") if (i["elementAttributeTypeId"]==343 and i["elementTypeKey"]=="responseCapture_metric_limit_policyExpiryDate")][0].get("value")
                    
                    adj_expdate = dt.datetime.strptime(adj_expdate[0:10], "%Y-%m-%d")
                    exp_expdate = dt.datetime.strptime(exp_expdate[0:10], "%Y-%m-%d")
                    
                    exp_hour = dt.datetime.strptime(contenido_json.get("expiryStartTime"), "%H:%M").hour
                    
                    quote_adj_expdate = adj_expdate + dt.timedelta(days=1) if exp_hour>=23 else  adj_expdate
                    overview_expdate = str(dt.datetime.strptime(contenido_json.get("expiryDate")[0:10], "%Y-%m-%d") + dt.timedelta(days=1) if exp_hour>=23 else dt.datetime.strptime(contenido_json.get("expiryDate")[0:10], "%Y-%m-%d"))[0:10]
                    
                    if str(quote_adj_expdate)[0:10] != overview_expdate:
                        print("\t\t- Validations:") 
                        print("\t\t\t- ERROR, The the dates of the overview [",overview_expdate,"] and responses [",str(quote_adj_expdate)[0:10],"], are different.")
                        pass
                    
                    #All OK, MTA Creation:
                    else:
                        print("\tMTA",j,"- Pol Reference:",MTAs[j].get("policyReference"))
                
                        #Pol_id por geografia:
                        if contenido_json.get("dataSourceId") == 50044 or contenido_json.get("dataSourceId") == 50041:
                            try:
                                root = ET.fromstring(MTAs[j].get("policyAttributeXML"))
                                print("\t- Local Pol_id :",root.find('POL_ID').text)
                            except:
                                print("\t- Local Pol_id : None",) 
                        else:
                            pass
    
                        print("\t- MTA_type:",contenido_json.get("mtaType"))
    
                        print("\t- Alias:","BKP_"+ contenido_json.get("placementKey"))
    
                        print("\t- MTA_Description: BKP_id:",contenido_json.get("placementName"))
    
                        #Evaluate if its the Lead Carrier.
                        print("\t\t- Lead Carrier:",lead_carrier,"-",lead_carrier_descp,"- Coas(%):",lead_carrier_perc,"%") 
    
                        #Permanent or Temporary Calculations:
                        if contenido_json.get("mtaTypeId") == 1:
                            ka = True
                        else:
                            ka = False
                        
                        #DATES:
    
                        #Effect Date:
                        mta_effectdate = contenido_json.get("inceptionDate")[0:10]
                        print("\t\t- MTA Effect date:", mta_effectdate)
    
                        #ExpiryDate:
                        print("\t\t- Policy Expiry date:", str(quote_adj_expdate)[0:10])
    
                        #QUOTE CHANGES:
                        print("\t\t- QUOTE_CHANGES:")
                        
                        
                        #Basis
                        if ka==True:
                           if is_leap_year(dt.datetime.strptime(mta_effectdate[0:10], "%Y-%m-%d").year):
                               y_basis = round(basis(366),4)
                               print("\t\t\tCalculated Basis : ", y_basis)
                           else:
                               y_basis = round(basis(365),4)
                               print("\t\t\tCalculated Basis : ", y_basis)
                        else: 
                            pass
                
                        #Prima Neta
    
                        delta_premium = round(delta_root("premium")* y_basis,2) if ka else round(delta_root("premium"),2)
                        print("\t\t\tdeltaPrimaNeta: ", delta_premium)
                
                        #Otros Impuestos:
                        delta_otrosimpuestos = round(delta_root("additionalPolicyCost") * y_basis,2) if ka else round(delta_root("additionalPolicyCost"),2)
                        print("\t\t\t- deltaOtrosImpuestos: ", delta_otrosimpuestos)
                
                        #Comisiones:
                        if delta_atributes_percentages("responseCapture_metric_commission") == 0 or delta_atributes_percentages("responseCapture_metric_commission") is None :
                            try:
                                deltacomisions=delta_atributes_amounts("responseCapture_metric_commission")
                            except:
                                deltacomisions=0
                        else: deltacomisions=delta_atributes_percentages("responseCapture_metric_commission")
                        
                        #print("\t\t\tdeltaComisiones: ", round(deltacomisions * y_basis,2) if ka else round(deltacomisions,2))
                        
                        #IPT:
                        if delta_atributes_percentages("responseCapture_metric_premium_insurancePremiumTax") == 0:
                            deltaipt=delta_atributes_amounts("responseCapture_metric_premium_insurancePremiumTax")
                        else: deltaipt=delta_atributes_percentages("responseCapture_metric_premium_insurancePremiumTax")
                
                        delta_ipt = round(deltaipt*y_basis,2) if ka else round(deltaipt,2)
                        print("\t\t\t- deltaIPT:", delta_ipt )
                
                        #Consorcio:
                        deltaConsorcio = delta_atributes_amounts("responseCapture_metric_consorcioContribution")
                        delta_Consorcio = round(deltaConsorcio*y_basis,2) if ka else round(deltaConsorcio,2)
                        print("\t\t\t- deltaConsorcio:",delta_Consorcio)
    
                        #Total Receipt:
                        totalrecibo = delta_premium + delta_otrosimpuestos + delta_ipt + delta_Consorcio
                        print("\t\t\tTotalRecibo:",round(totalrecibo,2))
    
                        #MTA Comments:
                        print("\t\t- MTA Comments: NULL",)
    else:
        print("This scenario is not covered, Placement Status: ", contenido_json.get("placementStatus"), "is incomplete.")
        pass
                    

            


            

                


                




