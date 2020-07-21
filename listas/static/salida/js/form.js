var tblProducts;
var vents = {
    items: {
        responsable: '',
        fecha: '',
        total: 0.00,
        products: []
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                {"data": "id"},
                {"data": "nombre"},
                {"data": "categoria"},
                {"data":"descripcion"},
                {"data": "cant"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                
                {
                    targets: [4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                
                
                
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000000000,
                    step: 1
                });

            },
            initComplete: function (settings, json) {

            }
        });
    },
};

$(function () {

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $('#fecha').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });


    // search products

    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            ui.item.cant = 1;
            console.log(vents.items);   
            vents.add(ui.item);
            $(this).val('');
        }
    });

    $('.btnRemoveAll').on('click', function () {
        if (vents.items.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            vents.items.products = [];
            vents.list();
        },function(){

        });
    });

    // event cant
    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
             function () {
                vents.items.products.splice(tr.row, 1);
                vents.list();
            }, function () {
            });
        })
        .on('change', 'input[name="cant"]', function () {
            console.clear();
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.items.products[tr.row].cant = cant;
            console.log(vents.items.products);
        });

    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    // event submit
    $('form').on('submit', function (e) {
        e.preventDefault();

        if(vents.items.products.length === 0){
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }

        vents.items.fecha = $('input[name="fecha"]').val();
        vents.items.responsable = $('select[name="responsable"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
        
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
                alert_action('Notificación', '¿Desea imprimir la boleta de Salida?', function () {
                    window.open('/bodegas/salida/invoice/pdf/' + response.id + '/', '_blank');
                    location.href = '/bodegas/salida/list/';
                }, function () {
                    location.href = '/bodegas/salida/list/';
                });
            });
    });
    
    
    function formatRepo(repo) {
        if (repo.loading) {
            return repo.text;
        }
    
        var option = $(
            '<div class="wrapper container">' +
            '<div class="row">' +
            '<div class="col-lg-1">' +
            '<img src="' + repo.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
            '</div>' +
            '<div class="col-lg-11 text-left shadow-sm">' +
            //'<br>' +
            '<p style="margin-bottom: 0;">' +
            '<b>Codigo:</b> ' + repo.codigo + '<br>' +
            '<b>Nombre:</b> ' + repo.nombre + '<br>' +
            '<b>Categoría:</b> ' + repo.categoria + '<br>' +
            '<b>stock::</b> <span class="badge badge-warning">#' + repo.total + '</span>' +
            '</p>' +
            '</div>' +
            '</div>' +
            '</div>');
    
        return option;
    }
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_products'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        data.cant = 1;
        data.subtotal = 0.00;
        vents.add(data);
        $(this).val('').trigger('change.select2');
    });
    vents.list();
});