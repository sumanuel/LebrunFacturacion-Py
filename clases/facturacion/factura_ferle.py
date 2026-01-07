import os
import logging
from datetime import datetime
from typing import Optional, Any

logger = logging.getLogger(__name__)

class FacturaFerle:
    """
    Clase para generar y imprimir facturas en formato texto plano para Ferreteria Ferle.
    Equivalente a la clase FacturaFerle.cs del proyecto original.
    """

    def __init__(self):
        self.texto_defaul_fav = self._get_default_template()
        self.texto_txt_fav = ""

    def _get_default_template(self) -> str:
        """Retorna el template por defecto de la factura."""
        return """

        %Cliente                                               %               %TipoDocumento% Nr.%NroDocum  %   Hora:%Hora    %
Rif:%NroRif              %   Nit:%NroNit              %
%DireccFiscal1                                            %          FECHA   :%FechEmisi%
%DireccFiscal2                                            %
Z.P.:%ZP%        Tlf.:%ATLF%-%Telefono           %
N/E.:%NOTAENTR%  Fec.N/E:%FECENTRE%                                    PEDIDO  : %NroPedido %
TD:%TDAPL% Aplica:%NRODOCAP% Control:%NROCOFAC% %FECFAC% Monto:%MONFAC% TRANSPORTE: %Transporte        % VENDEDOR: %CV%
%DireccEnvio                                                    %


                                                                                                 %Vienen...%       %Vienen         %
%Cod1  %    %Un1 % %Desc1                                             %      %Cant1  %      %Prec1       %  %A1 %  %Tot1           %
%Cod2  %    %Un2 % %Desc2                                             %      %Cant2  %      %Prec2       %  %A2 %  %Tot2           %
%Cod3  %    %Un3 % %Desc3                                             %      %Cant3  %      %Prec3       %  %A3 %  %Tot3           %
%Cod4  %    %Un4 % %Desc4                                             %      %Cant4  %      %Prec4       %  %A4 %  %Tot4           %
%Cod5  %    %Un5 % %Desc5                                             %      %Cant5  %      %Prec5       %  %A5 %  %Tot5           %
%Cod6  %    %Un6 % %Desc6                                             %      %Cant6  %      %Prec6       %  %A6 %  %Tot6           %
%Cod7  %    %Un7 % %Desc7                                             %      %Cant7  %      %Prec7       %  %A7 %  %Tot7           %
%Cod8  %    %Un8 % %Desc8                                             %      %Cant8  %      %Prec8       %  %A8 %  %Tot8           %
%Cod9  %    %Un9 % %Desc9                                             %      %Cant9  %      %Prec9       %  %A9 %  %Tot9           %
%Cod10 %    %Un10% %Desc10                                            %      %Cant10 %      %Prec10      %  %A10%  %Tot10          %
%Cod11 %    %Un11% %Desc11                                            %      %Cant11 %      %Prec11      %  %A11%  %Tot11          %
%Cod12 %    %Un12% %Desc12                                            %      %Cant12 %      %Prec12      %  %A12%  %Tot12          %
%Cod13 %    %Un13% %Desc13                                            %      %Cant13 %      %Prec13      %  %A13%  %Tot13          %
%Cod14 %    %Un14% %Desc14                                            %      %Cant14 %      %Prec14      %  %A14%  %Tot14          %
%Cod15 %    %Un15% %Desc15                                            %      %Cant15 %      %Prec15      %  %A15%  %Tot15          %
%Cod16 %    %Un16% %Desc16                                            %      %Cant16 %      %Prec16      %  %A16%  %Tot16          %
%Cod17 %    %Un17% %Desc17                                            %      %Cant17 %      %Prec17      %  %A17%  %Tot17          %
%Cod18 %    %Un18% %Desc18                                            %      %Cant18 %      %Prec18      %  %A18%  %Tot18          %
%Cod19 %    %Un19% %Desc19                                            %      %Cant19 %      %Prec19      %  %A19%  %Tot19          %
%Cod20 %    %Un20% %Desc20                                            %      %Cant20 %      %Prec20      %  %A20%  %Tot20          %
%Cod21 %    %Un21% %Desc21                                            %      %Cant21 %      %Prec21      %  %A21%  %Tot21          %
%Cod22 %    %Un22% %Desc22                                            %      %Cant22 %      %Prec22      %  %A22%  %Tot22          %
                   $bultosKilos                                                                               *raya

Si cancela de contado al recibir la mercanc¡a o antes del %FecDcto1% tendr  un %Pd1% de Dcto. adicional
     Mto. Factura Bs.   %  MontoSubTotd1%       I.V.A. %PorIvd1%%    %   MontoIvad1%            Total a Pagar     %    MontoTotald1%
Si cancela de contado al recibir la mercanc¡a o antes del %FecDcto2% tendr  un %Pd2% de Dcto. adicional
     Mto. Factura Bs.   %  MontoSubTotd2%       I.V.A. %PorIvd2%%    %   MontoIvad2%            Total a Pagar     %    MontoTotald2%
      %cheques
      BANCOS Y NUMEROS DE CUENTAS:
      BCO.VENEZUELA-CC.01020462310005459384 BCO.CARIBE-CC.01140161991610041023
      BCO.MERCANTIL-CC.01050026591026449715 BANESCO   -CC.01340379153791008610

-Emitir cheque  $$  unicamente  a nombre  de  FERRETERIA  FERLE  C.A.
-Favor revisar la mercancia a su entrega.No aceptamos reclamos despues de 10 dias
 habiles de haber sido recibida por el comprador.
-Como prueba de cancelacion, solo aceptamos los  recibos  numerados de Ferreteria IVA%PorcIva%%       %MontoSubTotal  %
 Ferle C.A., firmados por la(s) persona(s)autorizada(s).
-Para todos los efectos legales y comerciales, se elige como domicilio especial a
 la ciudad de Caracas.                                                                                            %      MontoTotal%
-La Mercancia viaja por cuenta y riesgo del comprador.
"""

    def imprimir_fav(self, factura: Any) -> None:
        """
        Imprime una factura (FAV).
        Args:
            factura: Objeto Factura con los datos necesarios.
        """
        try:
            self.texto_txt_fav = self.texto_defaul_fav

            # Reemplazos iniciales
            self.texto_txt_fav = self.texto_txt_fav.replace("%Vienen         %", " " * 17)
            self.texto_txt_fav = self.texto_txt_fav.replace("%Vienen...%", " " * 11)
            self.texto_txt_fav = self.texto_txt_fav.replace("%Van...%", " " * 8)
            self.texto_txt_fav = self.texto_txt_fav.replace("%Vienen...%", " " * 9)
            self.texto_txt_fav = self.texto_txt_fav.replace("%Vienen         %", " " * 17)

            self._cabecera_fav(factura)
            self._detalle_fav(factura)
            self._totales(factura)

            if factura.tiene_pp(factura):
                self._leyenda(True, factura)
            else:
                self._leyenda(False, factura)

            self._leyenda2(True)
            self._lpt()

            # Guardar archivo
            self._platilla_por_defecto()

        except Exception as e:
            logger.error(f"Error imprimiendo factura FAV: {e}")

    def imprimir_dev(self, factura: Any) -> None:
        """
        Imprime una nota de crédito (DEV).
        Args:
            factura: Objeto Factura con los datos necesarios.
        """
        try:
            self.texto_txt_fav = self.texto_defaul_fav

            # Reemplazos iniciales
            self.texto_txt_fav = self.texto_txt_fav.replace("%Vienen         %", " " * 17)
            self.texto_txt_fav = self.texto_txt_fav.replace("%Vienen...%", " " * 11)
            self.texto_txt_fav = self.texto_txt_fav.replace("%Van...%", " " * 8)
            self.texto_txt_fav = self.texto_txt_fav.replace("%Vienen...%", " " * 9)
            self.texto_txt_fav = self.texto_txt_fav.replace("%Vienen         %", " " * 17)

            self._cabecera_fav(factura)
            self._detalle_fav(factura)
            self._totales(factura)
            self._leyenda(False, factura)
            self._leyenda2(False)
            self._lpt()

            # Guardar archivo
            self._platilla_por_defecto()

        except Exception as e:
            logger.error(f"Error imprimiendo nota de crédito DEV: {e}")

    def _cabecera_fav(self, factura: Any) -> None:
        """Genera la cabecera de la factura."""
        try:
            # Obtener condición de pago
            from clases.complementos import CondicionPago
            cond_p = CondicionPago()
            dt_cond = cond_p.lbx_cond_pag()

            condicion_pago = ""
            dias = 0
            if dt_cond:
                for row in dt_cond:
                    if row.get('conp_codigo') == factura.cliente_facturar_prop.CondicionPago:
                        condicion_pago = row.get('conp_descripcion', '')
                        dias = int(float(row.get('conp_cant_dias', 0)))
                        break

            from datetime import datetime, timedelta
            fecha_vencimiento = datetime.now() + timedelta(days=dias)

            # Procesar nombre del cliente (quitar ñ)
            nombre_cliente = factura.cliente_facturar_prop.Nombre.replace('ñ', '¥').replace('Ñ', '¥')
            nombre_cliente = nombre_cliente[:50] if len(nombre_cliente) > 50 else nombre_cliente

            # Procesar direcciones
            direccion_fiscal = factura.cliente_facturar_prop.Direccion.replace('ñ', '¥').replace('Ñ', '¥')
            direccion_fiscal2 = getattr(factura.cliente_facturar_prop, 'Direccion2', '').replace('ñ', '¥').replace('Ñ', '¥')
            direccion_envio = getattr(factura.cliente_facturar_prop, 'DireccionEnvio', '').replace('ñ', '¥').replace('Ñ', '¥')

            # Reemplazos básicos
            tipo_doc = "FACTURA" if factura.tipo_documento_prop == "FAV" else "NOTA CREDITO"
            self.texto_txt_fav = self.texto_txt_fav.replace("%TipoDocumento%", tipo_doc)
            self.texto_txt_fav = self.texto_txt_fav.replace("%NroDocum  %", factura.correlativo_interno_prop)
            self.texto_txt_fav = self.texto_txt_fav.replace("%Hora    %", datetime.now().strftime("%H:%M"))

            # Cliente
            cliente_texto = f"{factura.cliente_facturar_prop.Codigo}-{nombre_cliente}"
            espacios = 56 - len(cliente_texto)
            self.texto_txt_fav = self.texto_txt_fav.replace("%Cliente                                               %",
                cliente_texto + " " * max(0, espacios))

            # Dirección fiscal 1
            dir1_texto = direccion_fiscal[:59] if len(direccion_fiscal) > 59 else direccion_fiscal
            espacios = 59 - len(dir1_texto)
            self.texto_txt_fav = self.texto_txt_fav.replace("%DireccFiscal1                                            %",
                dir1_texto + " " * max(0, espacios))

            # Dirección fiscal 2
            dir2_texto = direccion_fiscal2[:59] if len(direccion_fiscal2) > 59 else direccion_fiscal2
            espacios = 59 - len(dir2_texto)
            self.texto_txt_fav = self.texto_txt_fav.replace("%DireccFiscal2                                            %",
                dir2_texto + " " * max(0, espacios))

            # Dirección envío
            envio_texto = direccion_envio[:65] if len(direccion_envio) > 65 else direccion_envio
            self.texto_txt_fav = self.texto_txt_fav.replace("%DireccEnvio                                                    %", envio_texto)

            # RIF y NIT
            rif = getattr(factura.cliente_facturar_prop, 'Rif', '') or ""
            self.texto_txt_fav = self.texto_txt_fav.replace("%NroRif              %",
                rif + " " * max(0, 22 - len(rif)))

            nit = getattr(factura.cliente_facturar_prop, 'Nif', '') or ""
            self.texto_txt_fav = self.texto_txt_fav.replace("%NroNit              %",
                nit + " " * max(0, 22 - len(nit)))

            # Fecha emisión
            fecha_emision = datetime.now().strftime("%d/%m/%Y")
            self.texto_txt_fav = self.texto_txt_fav.replace("%FechEmisi%", fecha_emision)

            # Condición de pago
            cond_texto = condicion_pago[:20] if len(condicion_pago) > 20 else condicion_pago
            espacios = 20 - len(cond_texto)
            self.texto_txt_fav = self.texto_txt_fav.replace("%CondPago          %",
                cond_texto + " " * max(0, espacios))

            # Fecha vencimiento
            fecha_venc = fecha_vencimiento.strftime("%d/%m/%Y")
            self.texto_txt_fav = self.texto_txt_fav.replace("%FechVcmto%", fecha_venc)

            # Transporte
            transporte = getattr(factura.cliente_facturar_prop, 'Transporte', '') or ""
            transp_texto = transporte[:20] if len(transporte) > 20 else transporte
            espacios = 20 - len(transp_texto)
            self.texto_txt_fav = self.texto_txt_fav.replace("%Transporte        %",
                transp_texto + " " * max(0, espacios))

            # Vendedor
            vendedor_cod = getattr(factura.vendedor_factura_prop, 'CodigoV', '') or ""
            if len(vendedor_cod) > 7:
                vendedor_cod = vendedor_cod[7:]
            self.texto_txt_fav = self.texto_txt_fav.replace("%CV%", vendedor_cod)

            # Número de pedido
            pedido = getattr(factura, 'numero_pedido_prop', '') or ""
            self.texto_txt_fav = self.texto_txt_fav.replace("%NroPedido %", pedido)

            # Zona postal
            zp = getattr(factura.cliente_facturar_prop, 'ZonaPostal', '') or ""
            self.texto_txt_fav = self.texto_txt_fav.replace("%ZP%", str(zp))

            # Teléfono
            telefono = getattr(factura.cliente_facturar_prop, 'Telefono', '') or ""
            self.texto_txt_fav = self.texto_txt_fav.replace("%ATLF%-%Telefono           %", telefono)

            # Campos vacíos por defecto
            self.texto_txt_fav = self.texto_txt_fav.replace("%NOTAENTR%", " " * 10)
            self.texto_txt_fav = self.texto_txt_fav.replace("%FECENTRE%", " " * 10)
            self.texto_txt_fav = self.texto_txt_fav.replace("%TDAPL%", " " * 3)
            self.texto_txt_fav = self.texto_txt_fav.replace("%NRODOCAP%", " " * 10)
            self.texto_txt_fav = self.texto_txt_fav.replace("%NROCOFAC%", " " * 11)
            self.texto_txt_fav = self.texto_txt_fav.replace("%FECFAC%", " " * 10)
            self.texto_txt_fav = self.texto_txt_fav.replace("%MONFAC%", " " * 11)

        except Exception as e:
            logger.error(f"Error generando cabecera: {e}")

    def _detalle_fav(self, factura: Any) -> None:
        """Genera el detalle de items de la factura."""
        try:
            if not hasattr(factura, 'dgv_items') or factura.dgv_items is None:
                return

            items_df = factura.dgv_items
            raya = "------------------"
            bultos_pesos = "Bultos:$    Kilos:#"

            for i in range(len(items_df)):
                if i >= 22:  # Máximo 22 líneas en el template
                    break

                # Código
                codigo = items_df.iloc[i].get('@mov_codigo', '')
                if len(codigo) > 6:
                    codigo = codigo[6:]
                self.texto_txt_fav = self.texto_txt_fav.replace(f"%Cod{i+1}  %",
                    codigo + " " * max(0, 7 - len(codigo)))

                # Unidad
                unidad = items_df.iloc[i].get('@mov_undmed', '')
                unidad = unidad[:5] if len(unidad) > 6 else unidad
                espacios = 6 - len(unidad)
                self.texto_txt_fav = self.texto_txt_fav.replace(f"%Un{i+1} %",
                    " " * max(0, espacios) + unidad)

                # Descripción
                descripcion = items_df.iloc[i].get('@mov_memo', '')
                descripcion = descripcion[:51] if len(descripcion) > 52 else descripcion
                espacios = 52 - len(descripcion)
                self.texto_txt_fav = self.texto_txt_fav.replace(f"%Desc{i+1}                                             %",
                    " " * max(0, espacios) + descripcion)

                # Cantidad
                cantidad = str(items_df.iloc[i].get('@mov_cant', '0'))
                cantidad = cantidad[:8] if len(cantidad) > 9 else cantidad
                espacios = 9 - len(cantidad)
                self.texto_txt_fav = self.texto_txt_fav.replace(f"%Cant{i+1}  %",
                    " " * max(0, espacios) + cantidad)

                # Precio
                precio_val = float(items_df.iloc[i].get('@mov_precio', 0))
                precio = f"{precio_val:,.2f}"
                espacios = 14 - len(precio)
                self.texto_txt_fav = self.texto_txt_fav.replace(f"%Prec{i+1}       %",
                    " " * max(0, espacios) + precio)

                # IVA
                iva_val = float(items_df.iloc[i].get('@mov_porciva', 0))
                iva = f"{iva_val:,.2f}"
                espacios = 5 - len(iva)
                self.texto_txt_fav = self.texto_txt_fav.replace(f"%A{i+1} %",
                    " " * max(0, espacios) + iva)

                # Total
                total_val = float(items_df.iloc[i].get('@mov_total', 0))
                total = f"{total_val:,.2f}"
                espacios = 17 - len(total)
                self.texto_txt_fav = self.texto_txt_fav.replace(f"%Tot{i+1}           %",
                    " " * max(0, espacios) + total)

            # Reemplazar raya y bultos
            self.texto_txt_fav = self.texto_txt_fav.replace("*raya", raya)
            self.texto_txt_fav = self.texto_txt_fav.replace("$bultosKilos", bultos_pesos)

        except Exception as e:
            logger.error(f"Error generando detalle: {e}")

    def _totales(self, factura: Any) -> None:
        """Calcula y reemplaza los totales."""
        try:
            if not hasattr(factura, 'dgv_items') or factura.dgv_items is None or len(factura.dgv_items) == 0:
                return

            # Obtener porcentaje de IVA del primer item
            iva_porcentaje = float(factura.dgv_items.iloc[0].get('@mov_porciva', 0))
            iva_formateado = f"{iva_porcentaje:,.2f}"
            espacios = 9 - len(iva_formateado)
            self.texto_txt_fav = self.texto_txt_fav.replace("%PorcIva%",
                " " * max(0, espacios) + iva_formateado)

            es_nota_credito = factura.tipo_documento_prop.upper() == "DEV"

            if es_nota_credito:
                # Subtotal
                subtotal = f"{factura.total_base_prop:,.2f}"
                espacios = 16 - len(subtotal)
                self.texto_txt_fav = self.texto_txt_fav.replace("%MontoSubTotal  %",
                    " " * max(0, espacios) + "-" + subtotal)

                self.texto_txt_fav = self.texto_txt_fav.replace("%MontoSubTotal2 %",
                    " " * max(0, espacios) + "-" + subtotal)

                # IVA
                iva_total = f"{factura.iva_total_prop:,.2f}"
                espacios = 15 - len(iva_total)
                self.texto_txt_fav = self.texto_txt_fav.replace("%      MontoIva%",
                    " " * max(0, espacios) + "-" + iva_total)

                # Total
                total = f"{factura.total_neto_prop:,.2f}"
                espacios = 17 - len(total)
                self.texto_txt_fav = self.texto_txt_fav.replace("%      MontoTotal%",
                    " " * max(0, espacios) + "-" + total)
            else:
                # Subtotal
                subtotal = f"{factura.total_base_prop:,.2f}"
                espacios = 17 - len(subtotal)
                self.texto_txt_fav = self.texto_txt_fav.replace("%MontoSubTotal  %",
                    " " * max(0, espacios) + subtotal)

                self.texto_txt_fav = self.texto_txt_fav.replace("%MontoSubTotal2 %",
                    " " * max(0, espacios) + subtotal)

                # IVA
                iva_total = f"{factura.iva_total_prop:,.2f}"
                espacios = 16 - len(iva_total)
                self.texto_txt_fav = self.texto_txt_fav.replace("%      MontoIva%",
                    " " * max(0, espacios) + iva_total)

                # Total
                total = f"{factura.total_neto_prop:,.2f}"
                espacios = 18 - len(total)
                self.texto_txt_fav = self.texto_txt_fav.replace("%      MontoTotal%",
                    " " * max(0, espacios) + total)

        except Exception as e:
            logger.error(f"Error calculando totales: {e}")

    def _leyenda(self, valor: bool, factura: Any) -> None:
        """Genera la leyenda de pronto pago."""
        try:
            if not valor:
                # Limpiar leyendas de pronto pago
                self.texto_txt_fav = self.texto_txt_fav.replace(
                    "Si cancela de contado al recibir la mercanc¡a o antes del %FecDcto1% tendr  un %Pd1% de Dcto. adicional",
                    " " * 105)
                self.texto_txt_fav = self.texto_txt_fav.replace(
                    "Mto. Factura Bs.   %  MontoSubTotd1%       I.V.A. %PorIvd1%%    %   MontoIvad1%            Total a Pagar     %    MontoTotald1%",
                    " " * 127)
                self.texto_txt_fav = self.texto_txt_fav.replace(
                    "Si cancela de contado al recibir la mercanc¡a o antes del %FecDcto2% tendr  un %Pd2% de Dcto. adicional",
                    " " * 105)
                self.texto_txt_fav = self.texto_txt_fav.replace(
                    "Mto. Factura Bs.   %  MontoSubTotd2%       I.V.A. %PorIvd2%%    %   MontoIvad2%            Total a Pagar     %    MontoTotald2%",
                    " " * 127)
                self.texto_txt_fav = self.texto_txt_fav.replace(
                    "%cheques                                                                                   %",
                    " " * 92)
                self.texto_txt_fav = self.texto_txt_fav.replace("BANCOS Y NUMEROS DE CUENTAS:  ", " " * 30)
                self.texto_txt_fav = self.texto_txt_fav.replace(
                    "BCO.VENEZUELA-CC.01020462310005459384 BCO.CARIBE-CC.01140161991610041023",
                    " " * 72)
                self.texto_txt_fav = self.texto_txt_fav.replace(
                    "BCO.MERCANTIL-CC.01050026591026449715 BANESCO   -CC.01340379153791008610",
                    " " * 72)
            else:
                # Implementar lógica de pronto pago
                self.texto_txt_fav = self.texto_txt_fav.replace(
                    "%cheques                                                                                   %",
                    "Si su Cheque resulta devuelto por cualquier motivo debera Can.el monto mayor de la Factura")

                # Aquí iría la lógica completa de pronto pago
                # Por simplicidad, limpiamos los placeholders
                self.texto_txt_fav = self.texto_txt_fav.replace("%FecDcto1%", " " * 10)
                self.texto_txt_fav = self.texto_txt_fav.replace("%Pd1%", " " * 5)
                self.texto_txt_fav = self.texto_txt_fav.replace("%MontoSubTotd1%", " " * 15)
                self.texto_txt_fav = self.texto_txt_fav.replace("%PorIvd1%", " " * 5)
                self.texto_txt_fav = self.texto_txt_fav.replace("%MontoIvad1%", " " * 12)
                self.texto_txt_fav = self.texto_txt_fav.replace("%MontoTotald1%", " " * 15)
                self.texto_txt_fav = self.texto_txt_fav.replace("%FecDcto2%", " " * 10)
                self.texto_txt_fav = self.texto_txt_fav.replace("%Pd2%", " " * 5)
                self.texto_txt_fav = self.texto_txt_fav.replace("%MontoSubTotd2%", " " * 15)
                self.texto_txt_fav = self.texto_txt_fav.replace("%PorIvd2%", " " * 5)
                self.texto_txt_fav = self.texto_txt_fav.replace("%MontoIvad2%", " " * 12)
                self.texto_txt_fav = self.texto_txt_fav.replace("%MontoTotald2%", " " * 15)

        except Exception as e:
            logger.error(f"Error generando leyenda: {e}")

    def _leyenda2(self, valor: bool) -> None:
        """Genera la segunda leyenda."""
        try:
            if not valor:
                # Limpiar "Van..." para notas de crédito
                self.texto_txt_fav = self.texto_txt_fav.replace("%Van...%", " " * 8)
            else:
                # Mantener "Van..." para facturas
                pass
        except Exception as e:
            logger.error(f"Error generando leyenda2: {e}")

    def _lpt(self) -> None:
        """Envía el texto a la impresora LPT1."""
        # En Python, en lugar de CreateFile de Windows, usar una alternativa
        # Para compatibilidad, escribir a archivo o usar impresión genérica
        try:
            # Opción 1: Escribir a archivo
            with open("FAVFerle.txt", "w", encoding="utf-8") as f:
                f.write(self.texto_txt_fav)

            # Opción 2: Para impresión real, necesitaríamos una biblioteca
            # Por ahora, solo loggear
            logger.info("Factura preparada para impresión en FAVFerle.txt")

        except Exception as e:
            logger.error(f"Error enviando a impresora: {e}")

    def _platilla_por_defecto(self) -> None:
        """Guarda el template por defecto."""
        try:
            with open("FAVFerle.txt", "w", encoding="utf-8") as f:
                f.write(self.texto_defaul_fav)
        except Exception as e:
            logger.error(f"Error guardando template por defecto: {e}")